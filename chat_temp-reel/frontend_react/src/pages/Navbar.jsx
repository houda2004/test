import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        // Vérifier si un token existe pour déterminer si l'utilisateur est connecté
        const token = localStorage.getItem('token');
        setIsLoggedIn(!!token);
    }, []);

    const toggleMenu = () => {
        setIsOpen(!isOpen);
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        setIsLoggedIn(false);
        navigate('/');
    };

    return (
        <nav className="bg-blue-600 p-4 shadow-lg">
            <div className="max-w-7xl mx-auto flex justify-between items-center">
                {/* Logo */}
                <div className="text-white text-2xl font-bold">
                    MyApp
                </div>

                {/* Desktop Links */}
                <div className="hidden md:flex space-x-6">
                    <Link to="/" className="text-white hover:text-gray-200">Home</Link>
                    <Link to="/about" className="text-white hover:text-gray-200">About</Link>
                    <Link to="/contact" className="text-white hover:text-gray-200">Contact</Link>
                </div>

                {/* Auth Buttons */}
                <div className="hidden md:flex space-x-4">
                    {isLoggedIn ? (
                        <button onClick={handleLogout} className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-700">
                            Logout
                        </button>
                    ) : (
                        <Link to="/login" className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-700">
                            Login
                        </Link>
                    )}
                </div>

                {/* Mobile Menu Button */}
                <button onClick={toggleMenu} className="md:hidden text-white focus:outline-none">
                    {isOpen ? '✖️' : '☰'}
                </button>
            </div>

            {/* Mobile Menu */}
            {isOpen && (
                <div className="md:hidden flex flex-col bg-blue-700 p-4 space-y-2">
                    <Link to="/" className="text-white" onClick={toggleMenu}>Home</Link>
                    <Link to="/about" className="text-white" onClick={toggleMenu}>About</Link>
                    <Link to="/contact" className="text-white" onClick={toggleMenu}>Contact</Link>
                    {isLoggedIn ? (
                        <button onClick={handleLogout} className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-700">
                            Logout
                        </button>
                    ) : (
                        <Link to="/login" className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-700" onClick={toggleMenu}>
                            Login
                        </Link>
                    )}
                </div>
            )}
        </nav>
    );
};

export default Navbar;
