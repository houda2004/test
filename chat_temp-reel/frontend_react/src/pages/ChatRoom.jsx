import React, { useEffect, useState,useRef } from 'react';
import { FiSend, FiSearch, FiPaperclip,FiMic,FiTrash2, FiEdit3,FiMoreHorizontal,FiPlay, FiPause,FiDownload } from "react-icons/fi";
import { FaRegSmile } from "react-icons/fa";
import AudioMessage from './AudioMessage';
import Message from './message';
import { useNavigate } from 'react-router-dom';
const ChatWindow = ({ selectedRoom, combinedTimeline, personCurrent, onSendMessage }) => {   
    //const [audio, setAudio] = useState(null);
    const [SelectedMessageId, setSelectedMessageId] = useState(false);//pour delate ou modifait le message 

    const [file, setFile] = useState(null);

    const [audioBlob, setAudioBlob] = useState(null);// pour envoyer un fichier audio
    const [isRecording, setIsRecording] = useState(false);// pour la fonction de record audio
    const mediaRecorderRef = useRef(null); // pour la fonction de record audio
    const audioRef = useRef(null);// 
    const [isPlaying, setIsPlaying] = useState(false);
    const [audioURL, setAudioURL] = useState(''); // URL de l'audio enregistré pour la lecture
    const audioChunksRef = useRef([]); // Stocke les morceaux audio pendant l'enregistrement
    const [playingIndex, setPlayingIndex] = useState(null);

    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState(combinedTimeline);
    const [chatSocket, setChatSocket] = useState(null);
    const navigate = useNavigate();
    const messagesEndRef = useRef(null);//pour scroll automatiquement vers le bas

     // Scroll to bottom when a new message is added
     useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
     }, [messages]);

    const goToVideoCall=(idCall) => {
        navigate('/VideoCall', { state: { idCall } });
    };
    // Réinitialiser les messages quand la room change et reconnecter le socket
    useEffect(() => {
        if (selectedRoom) {
            setMessages(combinedTimeline); // Réinitialiser les messages avec la timeline de la nouvelle room
        }
    }, [selectedRoom, combinedTimeline]); // Dépendre de selectedRoom et combinedTimeline

    // Réinitialiser les messages quand la room change et reconnecter le socket
    useEffect(() => {
        // Fermer la connexion WebSocket précédente (si elle existe)
        if (chatSocket) {
            chatSocket.close();
        }
        if (!selectedRoom) return;
        const wsProtocol = window.location.protocol === "https:" ? "wss" : "ws";
        const socket = new WebSocket(`${wsProtocol}://${window.location.host}/ws/chat/${selectedRoom}/`);
//ws
        socket.onmessage = function (e) {
            const data = JSON.parse(e.data);
            if (data.action === "delete_message") {
               setMessages((prevMessages) => 
                prevMessages.filter(msg => msg.id !== data.message_id)
              );
            }else if(data.action === "update_message"){
                  setMessages((prevMessages) =>
                            prevMessages.map(msg => 
                              msg.id === data.message_id ? { ...msg, content: data.new_content } : msg
                            )
                          );
            }else{//"create message"
              /*let audioUrl = null;
              if (data.type_msg == "audio") {
                  //const audioBlob = new Blob([Uint8Array.from(atob(data.message), c => c.charCodeAt(0))], { type: "audio/wav" });
                  
                  // Décodage Base64 en Uint8Array
                      const binaryString = atob(data.message);
                      const byteArray = new Uint8Array(binaryString.length);
                      for (let i = 0; i < binaryString.length; i++) {
                        byteArray[i] = binaryString.charCodeAt(i);
                      }
                      
                      // Création du Blob
                      const audioBlob = new Blob([byteArray], { type: "audio/wav" });
                     console.log(audioBlob) 
                      console.log("📏 Taille du Blob reçu :", audioBlob.size, "octets");
                      audioUrl = URL.createObjectURL(audioBlob);
                     console.log(audioUrl)
                     setAudioURL(audioUrl)
                     console.log(audioURL)
                  // Ajouter l'URL audio au state des messages
                  //setMessages((prevMessages) => [...prevMessages, { type: "audio", audioUrl, sender: message.sender }]);
                  //content = audioUrl
              }*/
              setMessages(prevMessages => [
                ...prevMessages,
                  {
                    type: data.type,
                    type_msg:data.type_msg,
                    timestamp: data.timestamp, // Utiliser la date envoyée par le serveur
                    sender: data.sender_name,  // Remplace "sender" par "sender_name"
                    content: data.message,//data.type_msg == "audio" ? audioUrl :
                    id:data.id,
                    //fileName: data.fileName,
                    //audioData: data.audioData,           
                }
              ]);
            }
            console.log(data)
        };
                {/*
                    type: 'message',
                    timestamp: data.timestamp, // Utiliser la date envoyée par le serveur
                    sender: data.sender_name,  // Remplace "sender" par "sender_name"
                    content: data.message,*/
                }
        socket.onclose = function (event) {
            console.log("🔴 WebSocket fermé:", event);
            console.error('Chat socket closed unexpectedly');
            //setMessages('');
        };

        setChatSocket(socket);
       console.log(socket)
       return () => {
            socket.close();
           // setMessages('');
        };
    }, [selectedRoom]);

    const handleSend = () => {
        /*if (message.trim() && chatSocket) {
            chatSocket.send(JSON.stringify({
                message: message,
                sender: personCurrent
            }));
            setMessage('');
        }*/  let newMessage = null;
            if (message.trim() && chatSocket) {
                newMessage={
                    type: 'message',
                    type_msg: 'text',
                    message: message,//
                    sender: personCurrent,
                    action: "create message",
                    //timestamp: new Date().toISOString()
                };
                setMessage('');
            } else if (file) {
                newMessage={
                    type: 'message',
                    type_msg: 'file',
                    fileName: file.name,
                    sender: personCurrent,
                    action: "create message",
                    //timestamp: new Date().toISOString()
                };
                setFile(null);
            } /*else if (audioBlob) {
                const reader = new FileReader();
                reader.readAsDataURL(audioBlob);
                reader.onloadend = () => {
                    chatSocket.send(JSON.stringify({
                        type: 'message',
                        type_msg: 'audio',
                        audioData: reader.result,
                        sender: personCurrent
                    }));
                };
                setAudioBlob(null);
            }*/
            if (newMessage) {
                chatSocket.send(JSON.stringify(newMessage));
                //setMessages(prevMessages => [...prevMessages, newMessage]);
            }
            console.log(newMessage)
            console.log(chatSocket)
    };
    // Gérer l'upload de fichier (accepter uniquement les PDF)
    const handleFileUpload = (event) => {
        //setFile(event.target.files[0]);
        const selectedFile = event.target.files[0];
       if (selectedFile.type === 'application/pdf') {
        setFile(selectedFile);
       } else {
        alert('Only PDF files are allowed.');
       }
    };


    const startRecording = async () => {//toggleRecordingisRecording
       navigator.mediaDevices
             .getUserMedia({ audio: true })
             .then((stream) => {
               mediaRecorderRef.current = new MediaRecorder(stream);
               mediaRecorderRef.current.ondataavailable = (event) => {
                audioChunksRef.current.push(event.data);
               };
               mediaRecorderRef.current.onstop = () => {
                 const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
                  const reader = new FileReader();
                  reader.readAsDataURL(audioBlob);
                  reader.onloadend = () => {
                      const base64Audio = reader.result.split(',')[1]; // Récupérer seulement la partie Base64
                
                        chatSocket.send(JSON.stringify({
                          type: 'message',
                          type_msg: "audio",
                          audioData: base64Audio, // Envoi du fichier encodé en Base64
                          sender: personCurrent,
                          action: "create message",
                        }));
                        console.log(base64Audio)
                      };
                
                      setIsRecording(false);
                    };
                
       
               mediaRecorderRef.current.start();
               setIsRecording(true);
               setTimeout(() => {
                mediaRecorderRef.current.stop();
                setIsRecording(false);
              }, 7000); // Enregistre pendant 7 secondes
               
             })
             .catch((error) => console.error("Erreur d'accès au microphone : ", error));
       
    };

    // Fonction pour arrêter l'enregistrement audio
      const stopRecording = () => {
        mediaRecorderRef.current.stop(); // Arrêter l'enregistrement
        setIsRecording(false); // Mettre à jour l'état pour indiquer que l'enregistrement est terminé
      };

    const togglePlay = (audioUrl,index) => {//palye audio 
        if (audioRef.current && audioRef.current.src === audioUrl) {
            if (isPlaying) {
                audioRef.current.pause();
            } else {
                audioRef.current.play();
            }
            setIsPlaying(!isPlaying);
        } else {
            if (audioRef.current) {
                audioRef.current.pause();
            }
            audioRef.current = new Audio(audioUrl);
            audioRef.current.play();
            setIsPlaying(true);
        }
    };

    //////////////////
    // Toggle visibility of options box
  const handleMoreClick = (messageId) => {
    
    // Toggle visibility for the clicked message's options
    setSelectedMessageId(SelectedMessageId === messageId ? null : messageId);
  };

  // Placeholder functions for "Delete" and "Pin" actions
  const handleDelete = async (messageId) => {
    /*try {
      await axios.delete(`http://127.0.0.1:8000/api/messages/${messageId}/`);
      alert("Message Delete");
      // Mettre à jour l'état local en filtrant le message supprimé
      //setMessages((prevMessages) => prevMessages.filter(msg => msg.id !== messageId));
    } catch (error) {
      console.error("Erreur lors de la suppression :", error);
    }*/
      chatSocket.send(JSON.stringify({
        type: 'message',
        action: "delete_message",
        message_id: messageId
      }));
  };

const handleEdit = async (messageId, newContent) => {
  /*try {
    const response = await axios.patch(`http://127.0.0.1:8000/api/messages/${messageId}/`, {
      content: newContent,
      pinned: true // Ajoute un champ "pinned" si nécessaire
    });

    // Mettre à jour l'état local pour refléter le changement
    setMessages((prevMessages) =>
      prevMessages.map(msg => 
        msg.id === messageId ? { ...msg, content: newContent, pinned: true } : msg
      )
    );
    alert("Message pinned");
  } catch (error) {
    console.error("Erreur lors de la modification :", error);
  }*/
   const newText = prompt("Modifier le message :");
       if (newText) {
        chatSocket.send(JSON.stringify({
           type: 'message',
           action: "update_message",
           message_id: messageId,
           new_content: newText
         }));
       }
};

    return (
        <div className="room_content card flex flex-col h-full overflow-hidden">{/**room_content card  h-screen */}
            <div className="card-body flex-1 space-y-4 overflow-y-auto overflow-hidden">{/**h-4/5 card-body flex flex-col*/}
                {/*<div id="chat" className="flex-1 space-y-4">*/}
                
                {/* Chat Messages */}
                {messages.map((event, index) => (
                  <div key={index} className={`event mb-3 w-full ${event.sender === personCurrent ? 'flex justify-end' : 'flex justify-start'}`}>
                    {/* Handle message/text and file types */}
                    {event.type === 'chat_message' || event.type === 'message' ? (
                      <div>
                        {event.type_msg === 'text' ? (
                          <Message
                            sender={event.sender}
                            timestamp={event.timestamp}
                            content={event.content}
                            isCurrentUser={event.sender === personCurrent}
                          />
                        ) : event.type_msg === 'audio' ? (
                          <div className="audio-message p-3 border rounded-lg bg-gray-100">
                            {/*<div className="flex items-center space-x-2">
                              <button className="text-white" onClick={() => togglePlay(event.content,index)}>
                                {isPlaying ? <FiPause size={24} /> : <FiPlay size={24} />}
                              </button>
                              <audio ref={audioRef} src={event.content} className="hidden" type="audio/wav" controls />
                              <span>🎵 Audio Message</span>${isPlaying ? "block" : "hidden"}*/}
                              {/*<div className={`mt-2`}>
                                  <canvas ref={canvasRef} width={200} height={50}></canvas>
                              </div>
                            </div>*/}
                            {/*<AudioMessage audioUrl={event.content} index={index} />*/}
                              <AudioMessage 
                                  key={index}
                                  audioUrl={event.content}
                                  index={index}
                                  playingIndex={playingIndex}
                                  setPlayingIndex={setPlayingIndex}
                              />
                          </div>
                          
                        ) : event.type_msg === 'file' ? (
                          <div className="file-message p-3 border rounded-lg bg-gray-100">
                            <p>
                              <i className="fa-solid fa-file"></i>
                              <strong>{event.sender}</strong> sent a file
                            </p>
                            <a href={`/media/uploads/${event.content}`} download={event.content} className="btn btn-primary mt-2">
                              <FiDownload size={30} color="blue" />
                            </a>
                          </div>
                        ) : null}
                        {/* Options box (conditionally rendered) */}
                        <div>
                          <FiMoreHorizontal onClick={() => handleMoreClick(event.id)} className="cursor-pointer" />
                          {SelectedMessageId === event.id && (
                            <div className="absolute bg-white shadow-lg rounded-md p-2 mt-2 right-0">
                              <button
                                onClick={() => handleDelete(event.id)}
                                className="w-full text-red-500 text-sm p-2 hover:bg-gray-200 rounded flex justify-around items-end"
                              >
                                <FiTrash2 /> <span>Delete</span>
                              </button>
                              <button
                                onClick={() => handleEdit(event.id)}
                                className="w-full text-blue-500 text-sm p-2 hover:bg-gray-200 rounded flex justify-around items-end"
                              >
                                <FiEdit3 /> <span>Edit</span>
                              </button>
                            </div>
                          )}
                        </div>
                      </div>
                    ) : (
                      <div className="video_call p-3 border rounded-lg bg-gray-100">
                        <p>
                          <i className="fa-solid fa-phone"></i>
                          <strong>{event.caller}</strong> started a call
                        </p>
                        <p><small>Start Time: {event.start_time}</small></p>
                        {event.end_time ? (
                          <p><small>End Time: {event.end_time}</small></p>
                        ) : (
                          <p>Status: {event.status}</p>
                        )}
                        {/* button to join the call */}
                        {!event.end_time && (
                          <button onClick={() => goToVideoCall(event.id)} className="btn btn-success mt-2">Join Call</button>
                        )}
                      </div>
                    )}
                  </div>
                ))}
                {/* Auto scroll to latest message */}
                <div ref={messagesEndRef} />
                {/*</div>*/}
            </div>
            {/** end le la zone des messages */}
            
             {/* Box pour envoyer un message */}
            <div className="footer_room flex w-full card-footer sticky p-4 bg-white border-t-4 items-center shadow-md rounded-t-lg">{/**d-flex border-t border-gray-200 p-4 bg-gray-100  */}
                <input type="file" className="hidden" id="fileUpload" accept="application/pdf" onChange={handleFileUpload} />
                <label htmlFor="fileUpload">
                    <FiPaperclip className="text-gray-500 mr-2 cursor-pointer" />
                </label>
               {/** <FiMic className={`text-gray-500 mr-2 cursor-pointer ${isRecording ? 'text-red-500' : ''}`} onClick={toggleRecording} /> 
                * 
                * <FiMic
                    className={`text-gray-500 mr-2 cursor-pointer ${isRecording ? 'text-red-500' : ''}`}
                    onMouseDown={() => toggleRecording(true)}
                    onMouseUp={() => toggleRecording(false)}
                />
               */} 
                {!isRecording ? (
                          // Bouton pour démarrer l'enregistrement
                          <button onClick={startRecording}> 
                            <FiMic  className="text-gray-500 mr-2 cursor-pointer" />
                          </button>                         
                        ) : (
                          // Bouton pour arrêter l'enregistrement
                          <button onClick={stopRecording}>
                            <FiMic  className="mr-2 cursor-pointer text-red-500" />
                          </button>               
                        )} 
               <input
                  type="text"
                  className="w-full p-3 rounded-lg border border-gray-300 bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Type your message..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                />
                 <button
                        className="ml-3 px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                      onClick={handleSend}
                 >
                        <FiSend />
                </button>
            </div>
            {/** end box pour envoyer un message */}
            
        </div>
    );
};


export default ChatWindow;


