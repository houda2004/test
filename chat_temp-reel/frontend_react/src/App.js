
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';// pour utliser les routes et accisse ves les pages
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import RegisterForm from './pages/RegisterPage';
import axios from "axios";
import { useEffect, useState } from "react";
function App() { const [message, setMessage] = useState("");

  const getMessage = () => {
      axios.get("http://127.0.0.1:8000/Personnale/message/")
          .then(response => {
              setMessage(response.data.message);
          })
          .catch(error => {
              console.error("Erreur lors de la récupération du message:", error);
          });
  };

  return (
      <div>
          <h1>Message depuis Django:</h1>
          <p>{message}</p>
          <button onClick={getMessage}>Obtenir le Message</button>
      </div>
  );
}
/*
 <BrowserRouter>
            <Routes>
                <Route path="/login" element={<LoginPage />} />  
                <Route path="/" element={<HomePage />} />
                <Route path="/register" element={<RegisterForm />} />
            </Routes>
    </BrowserRouter>

*/ 
export default App;
