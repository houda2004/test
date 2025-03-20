import Navbar from './Navbar';
import RegisterForm from './RegisterPage';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
    const navigate = useNavigate();

    const goToRegister = () => {
        navigate('/register');
    };
    const goToContacts=() => {
        navigate('/MyContactes');
    }
    return (
         
        <div className="flex items-center justify-center h-screen bg-green-100">
            <div>
               <Navbar />
            </div>
            <button onClick={goToRegister} className="bg-blue-500 text-white p-2 rounded">
                Aller à la page d'inscription
            </button>
            <h1 className="text-3xl font-bold">Welcome to the Home Page! 🎉</h1>
            
            <button onClick={goToContacts} className="bg-blue-500 text-white p-2 rounded">
                Aller à la page des Contacts
            </button>
        </div>
    );
};

export default HomePage;
