
import React, { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

//toast.configure();
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.withCredentials = true;

const RegisterForm = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        confirm_password: '',
        code: '',
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const sendCode = async () => {
        try {
            const response = await axios.post('http://localhost:8000/Personnale/register/', { ...formData, send_code: true });
            toast.success(response.data.message);
        } catch (error) {
            toast.error(error.response?.data?.error || 'Failed to send code');
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/Personnale/register/', { ...formData, sign_up: true });
            toast.success(response.data.message);
        } catch (error) {
            toast.error('Registration failed');
        }
    };

    return (
        <div className="p-4">
            <h2 className="text-xl mb-4">Register</h2>
            <form onSubmit={handleSubmit} className="space-y-3">
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleChange}
                    className="border p-2 w-full"
                />
                
                <input
                    type="text"
                    name="code"
                    placeholder="Verification Code"
                    value={formData.code}
                    onChange={handleChange}
                    className="border p-2 w-full"
                />
                <button name='send_code' type="button" onClick={sendCode} className="bg-green-500 text-white p-2 rounded">Send Code</button>
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={handleChange}
                    className="border p-2 w-full"
                />
                <input
                    type="password"
                    name="confirm_password"
                    placeholder="Confirm Password"
                    value={formData.confirm_password}
                    onChange={handleChange}
                    className="border p-2 w-full"
                />
                <button name="sign_up" type="submit" className="bg-blue-500 text-white p-2 rounded">Sign Up</button>
            </form>
        </div>
    );
};

export default RegisterForm;
