import { useState } from 'react'
import './App.css'

const UNKNOWN_ERROR = "Я не знаю сколько это"
const operators = ["+", "-", "/", "*"]
const server_url = "http://85.93.56.121:8080"

function App() {
  const [expression, setExpression] = useState("0")
  const [result, setResult] = useState(null)
  const [mode, setMode] = useState(0)
  let [next_remove, setNextRemove] = useState(true)

  const SmartSetExpression = (value) => {
    if (value !== "") {
      if (expression !== "0") {
        if (expression !== UNKNOWN_ERROR) {
          setExpression(value)
        } else {
          setExpression(value.slice(UNKNOWN_ERROR.length, UNKNOWN_ERROR.length+1))
        }
      } else {
        setExpression(value.slice(1, 2))
      }
    } else {
      setExpression("0")
    }
    setNextRemove(false)
  }

  const AddToExpression = (symbol) => {
    if (next_remove !== true) {
      const new_expression = expression + symbol
      SmartSetExpression(new_expression)
    } else if (!operators.includes(symbol) || expression == UNKNOWN_ERROR) {
      setExpression(symbol)
      setNextRemove(false)
    }
  }

  const RemoveOneFromExpression = () => {
    const new_expression = expression.slice(0, -1)
    if (new_expression !== "") {
      setExpression(new_expression)
    } else {
      setExpression("0")
    }
  }

  const ClearExpression = () => {
    setExpression("0")
  }

  const handleCalculate = async () => {
    try {
      const response = await fetch(`${server_url}/calculate?expr=${encodeURIComponent(expression)}`)
      const data = await response.json()
      setExpression(data.result)
      setNextRemove(true)
    } catch (error) {
      console.error("Ошибка при запросе к API", error)
    }
  }

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault()

      if (expression !== UNKNOWN_ERROR) {
        handleCalculate()
      }
    }
  };

  const ChangeModeTo = (mode) => {
    setMode(mode)
    if (mode == 0 && expression.includes("=")) {
      setExpression(expression.slice(0, expression.indexOf("=")) )
    }
  }

  const Teach = async () => {
    if (!expression.includes("=")) {
      alert("Выражение должно содержать знак '='")
      return
    }
    try {
      const expression_to_send = expression.slice(0, expression.indexOf("=")) 
      const result_to_send = expression.slice(expression.indexOf("=")+1, expression.length) 
      console.log(expression_to_send, result_to_send)
      const response = await fetch(`${server_url}/teach`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "expression": expression_to_send, "result": result_to_send }),
      })
      const data = await response.json()
    } catch (error) {
      console.error("Ошибка при запросе к API", error)
    }
  }

  return (
    <div className="app-background">
      <h1>Chaos Calculator</h1>
      <div className="calculator-card">
        <div>
          <button className={mode === 1 ? "mode-btn" : "active-mode-btn"} onClick={() => ChangeModeTo(0)}>Счет</button>
          <button className={mode === 0 ? "mode-btn" : "active-mode-btn"} onClick={() => ChangeModeTo(1)}>Обучение</button>
        </div>
        <input 
          type="text" 
          value={expression} 
          onChange={(e) => SmartSetExpression(e.target.value)}
          onKeyDown={handleKeyDown} 
          placeholder="Выражение"
          className="output"
        />

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
          {mode == 0 && <button className="equal-btn" onClick={handleCalculate}>=</button>}
          {mode == 1 && <button className="equal-btn" onClick={() => AddToExpression("=")}>=</button>}
          <button className="operation-btn" onClick={() => AddToExpression("+")}>+</button>
        </div>

        {mode == 1 && <button className="teach-btn" onClick={Teach}>Обучить</button>}
      </div>
    </div>
  )
}

export default App