import { useState } from 'react'
import './App.css'

const server_url = "http://85.93.56.121:8080"

function App() {
  const [expression, setExpression] = useState("")
  const [mode, setMode] = useState(0)

  const AddToExpression = (symbol) => {
    setExpression(expression + symbol)
  }

  const RemoveOneFromExpression = () => {
    if (expression.length === 0) return
    setExpression(expression.slice(0, -1))
  }

  const ClearExpression = () => {
    setExpression("")
  }

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault()
      handleCalculate()
    }
  }

  const ChangeModeTo = (newMode) => {
    setMode(newMode)
  }

  const Teach = async () => {
    if (!expression.includes("=") || expression.split('=').length > 2) {
      alert("Выражение должно содержать ровно 1 знак '='")
      return
    }
    try {
      const expression_to_send = expression.slice(0, expression.indexOf("=")) 
      const result_to_send = expression.slice(expression.indexOf("=")+1) 
      
      await fetch(`${server_url}/teach`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "expression": expression_to_send, "result": result_to_send }),
      })
    } catch (error) {
      console.error("Ошибка при запросе к API", error)
    }
  }

  const handleCalculate = async () => {
    if (expression.includes("=")) {
      alert("Выражение не должно содержать знак '='")
      return
    }
    try {
      const response = await fetch(`${server_url}/calculate?expr=${encodeURIComponent(expression)}`)
      const data = await response.json()
      setExpression(data.result)
    } catch (error) {
      console.error("Ошибка при запросе к API", error)
    }
  }

  return (
    <div className="app-background">
      <h1>Chaos Calculator</h1>
      
      <div className="calculator-card">
        {/* Переключатель режимов */}
        <div className="mode-buttons">
          <button className={`mode-btn ${mode === 0 ? 'active' : ''}`} onClick={() => ChangeModeTo(0)}>
            Счет
          </button>
          <button className={`mode-btn ${mode === 1 ? 'active' : ''}`} onClick={() => ChangeModeTo(1)}>
            Обучение
          </button>
        </div>

        {/* Экран ввода */}
        <input 
          type="text" 
          value={expression} 
          onChange={(e) => setExpression(e.target.value)}
          onKeyDown={handleKeyDown} 
          placeholder="Введите выражение..."
          className="output"
        />  

        {/* Сетка кнопок */}
        <div className="buttons-grid">
          <button className="clear-btn" onClick={ClearExpression}>C</button>
          <button className="bracket-btn" onClick={() => AddToExpression("(")}>(</button>
          <button className="bracket-btn" onClick={() => AddToExpression(")")}>)</button>
          <button className="ac-btn" onClick={RemoveOneFromExpression}>⌫</button>

          <button className="number-btn" onClick={() => AddToExpression("7")}>7</button>
          <button className="number-btn" onClick={() => AddToExpression("8")}>8</button>
          <button className="number-btn" onClick={() => AddToExpression("9")}>9</button>
          <button className="operation-btn" onClick={() => AddToExpression("/")}>/</button>

          <button className="number-btn" onClick={() => AddToExpression("4")}>4</button>
          <button className="number-btn" onClick={() => AddToExpression("5")}>5</button>
          <button className="number-btn" onClick={() => AddToExpression("6")}>6</button>
          <button className="operation-btn" onClick={() => AddToExpression("*")}>*</button>

          <button className="number-btn" onClick={() => AddToExpression("1")}>1</button>
          <button className="number-btn" onClick={() => AddToExpression("2")}>2</button>
          <button className="number-btn" onClick={() => AddToExpression("3")}>3</button>
          <button className="operation-btn" onClick={() => AddToExpression("-")}>-</button>

          <button className="dot-btn" onClick={() => AddToExpression(".")}>.</button>
          <button className="number-btn" onClick={() => AddToExpression("0")}>0</button>
          
          {mode === 0 ? (
            <button className="equal-btn" onClick={handleCalculate}>=</button>
          ) : (
            <button className="equal-btn" onClick={() => AddToExpression("=")}>=</button>
          )}
          
          <button className="operation-btn" onClick={() => AddToExpression("+")}>+</button>
        </div>

        {/* Кнопка действия для обучения */}
        {mode === 1 && (
          <button className="teach-btn" onClick={Teach}>Обучить</button>
        )}
      </div>
    </div>
  )
}

export default App