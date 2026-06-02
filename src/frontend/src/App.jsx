import { useState } from 'react'
import './App.css' // Сюда потом напишем стили

function App() {
  // 1. Место для переменных (State)
  // В React нельзя просто написать expr = "2+2", 
  // нужно использовать useState, чтобы при изменении переменной обновлялся экран
  const [expression, setExpression] = useState("")
  const [result, setResult] = useState(null)

  // 2. Место для функций (Логика)
  const handleCalculate = async () => {
    // Внимание: мы обращаемся к твоему FastAPI, а не к БД напрямую!
    // Запросы к БД делает только бэкенд.
    try {
      const response = await fetch(`http://85.93.56.121:8080/calculate?expr=${encodeURIComponent(expression)}`)
      const data = await response.json()
      setResult(data.result)
    } catch (error) {
      console.error("Ошибка при запросе к API", error)
    }
  }

  // 3. Место для визуала (HTML)
  return (
    <div className="app-background">
      <div className="calculator-card">
        <h1>Chaos Calc</h1>
        
        {/* Поле ввода */}
        <input 
          type="text" 
          value={expression} 
          onChange={(e) => setExpression(e.target.value)} 
          placeholder="Введи 2+2"
        />

        {/* Кнопка */}
        <button onClick={handleCalculate}>
          Посчитать
        </button>

        {/* Вывод результата: показываем, только если result не null */}
        {result !== null && (
          <div className="result-box">
            Результат: {result}
          </div>
        )}
      </div>
    </div>
  )
}

export default App