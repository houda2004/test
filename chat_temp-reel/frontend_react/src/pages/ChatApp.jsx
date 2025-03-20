// on affiche les contacte et les chat de chaque room si on a choisier une room

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ContactList from './ContactList';
import ChatWindow from './ChatRoom';
import Navbar from './Navbar';
import { useNavigate } from "react-router-dom";
import {FaVideo } from 'react-icons/fa';
import CreateVideoCall from './CreateVideoCall';
const ChatApp = () => {
    const [rooms, setRooms] = useState([]);
    const [selectedRoom, setSelectedRoom] = useState(null);
    const [combinedTimeline, setCombinedTimeline] = useState([]);
    const [personCurrent, setPersonCurrent] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const [isVideoCallVisible, setIsVideoCallVisible] = useState(false);

    const fetchRooms = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/Contactes/');
            console.log('Données reçues:', response.data);  // Vérifier les données reçues
            setRooms(response.data.rooms);
            setPersonCurrent(response.data.person_current);
        } catch (error) {
            console.error('Erreur lors de la récupération des contacts:', error);
        }
    };

    useEffect(() => {
        fetchRooms();
    }, []);

    const handleRoomSelect = async (roomId) => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/Contactes/${roomId}/`);
            console.log('Room details response:', response.data); // Debugging
            setSelectedRoom(roomId);
            setCombinedTimeline(response.data.combined_timeline);
        } catch (error) {
            console.error('Error fetching room details:', error);
        }
    };
    

    // Fonction pour afficher la vidéo
      const handleCreateCall = () => {
        setIsVideoCallVisible(true);
      };
    
      // Fonction pour fermer la vidéo
      const handleCloseCall = () => {
        setIsVideoCallVisible(false);
      };

    /*const handleSendMessage = async (message) => {
        try {
            await axios.post('/api/send_message/', {
                room_id: selectedRoom,
                message: message
            });
            // Refresh the timeline after sending a message
            handleRoomSelect(selectedRoom);
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };*/
 /* <ul>
                {rooms.map((room) => (
                    <li key={room.id} onClick={() => handleRoomSelect(room.id)}>
                        {room.other_user}
                    </li>
                ))}
            </ul>*/
    return (
      
        <div className="base h-screen p-4">
          <div className="w-3/4 h-full bg-white shadow-lg rounded-lg flex overflow-hidden">
            {/* Left Side - 40% de la largeur h-screen*/}
            <div className="w-1/4 bg-gray-150 p-4 bg-blue-100 rounded-b-lg border-b border-gray-200 shadow-md rounded-lg">
                <h2 className="text-xl font-bold m-4">Contacts</h2>
                <hr></hr>
                <ContactList rooms={rooms} onRoomSelect={handleRoomSelect} />
            </div>

            {/* Right Side - 60% de la largeur */}
            <div className="w-3/4 bg-white h-full col-span-2 rounded-lg"> 
              {selectedRoom ? (
                <div className="flex flex-col h-full">
                  {/* Header (sticky en haut) */}
                   <div className="border-b-4 border-gray-200 sticky top-0 z-10 flex items-end space-x-2 p-4 bg-white shadow-md flex items-center">
                         <div>
                           <img src="https://www.bigfootdigital.co.uk/wp-content/uploads/2020/07/image-optimisation-scaled.jpg"  alt="User" class={`w-8 h-8 rounded-full`}></img>             
                           <h3 className="text-lg font-semibold">Conversation avec {selectedRoom.other_user}</h3>
                         </div>      
                        <div>
                              <button
                                onClick={handleCreateCall}
                                disabled={loading}
                                className="text-blue-500 hover:text-blue-700 transition duration-200"
                              >
                                <FaVideo size={24} />
                              </button>
                        
                              {/* Le composant CreateVideoCall qui s'affiche de façon absolue */}
                              {isVideoCallVisible && (
                                <div className="absolute top-1/5 left-1/5 z-50 bg-white p-5 rounded-lg shadow-lg">
                                  {/* Affiche le composant vidéo ou un contenu quelconque ici */}
                                  <CreateVideoCall roomId={selectedRoom} />
                        
                                  {/* Bouton pour fermer le composant */}
                                  <button onClick={handleCloseCall} className="mt-4 text-red-500 hover:text-red-700">
                                    Fermer la vidéo
                                  </button>
                                </div>
                              )}
                          </div>
                   </div>
                   {/* Conteneur de messages */}
                   <div className="pb-4 overflow-hidden"> {/* Conteneur de messages avec scroll border-b border-gray-200 pb-4 mb-4*/}        
                         <ChatWindow
                           combinedTimeline={combinedTimeline}
                           personCurrent={personCurrent}
                            selectedRoom={selectedRoom}
                        />
                   </div>
                 </div>
                ) : (
                        <p className="text-gray-500">Sélectionnez un contact pour afficher la discussion.</p>
                )}          
            </div>

        </div>
        
    </div>
    );
};
export default ChatApp;