import React, { useEffect, useState,useRef } from "react";
import AgoraRTC from "agora-rtc-sdk-ng";
import CosmosNodeNetwork from "./CosmosNodeNetwork";
//import { VideoCameraIcon, VideoCameraOffIcon, MicrophoneIcon, MicrophoneOffIcon } from '@heroicons/react/solid';
//import { VideoCameraIcon, MicrophoneIcon } from '@heroicons/react/24/solid';
//import { VideoCameraOffIcon, MicrophoneOffIcon } from '@heroicons/react/24/outline'; // Importation depuis `outline` pour les icônes "off"
//import "./VideoChat.css";
import {FaPhoneAlt ,FaVideo, FaMicrophone, FaVideoSlash, FaMicrophoneSlash } from 'react-icons/fa'; // Importer des icônes de FontAwesome
import { MdVideoCall, MdMic, MdMicOff } from 'react-icons/md'; // Importer des icônes de Material Design

import axios from "axios";
import { useLocation } from "react-router-dom";
const APP_ID = "b4ec67d6d68743cd83cba0ee704c55ac";  // Remplace par ton App ID Agora
//const client = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" });

const DEFAULT_PROFILE_PIC="https://www.bigfootdigital.co.uk/wp-content/uploads/2020/07/image-optimisation-scaled.jpg"
const TOKEN = null;
const VideoCall = () => {
    const location = useLocation();
    const { idCall } = location.state || {}; // Récupérer l'ID de l'appel
    const CHANNEL = "" + idCall;
    const [token, setToken] = useState(null);
    const client = useRef(null); // 🔥 On utilise useRef pour stocker le client Agora
    const localPlayerRef = useRef(null);
    const remotePlayerRef = useRef(null); // Référence pour le conteneur vidéo distant

    const [localTracks, setLocalTracks] = useState({ videoTrack: null, audioTrack: null });
    const [remoteUsers, setRemoteUsers] = useState({});
    const [joined, setJoined] = useState(false);
    const [userCount, setUserCount] = useState(0); // 🔥 Nombre de participants
    const [isVideoEnabled, setIsVideoEnabled] = useState(true);  // Caméra activée par défaut
    const [isAudioEnabled, setIsAudioEnabled] = useState(true);  // Micro activé par défaut
    //const [profilePicURL, setprofilePicURL] = useRef(null);
    // Image de profil par défaut
    const DEFAULT_PROFILE_PIC = "https://www.bigfootdigital.co.uk/wp-content/uploads/2020/07/image-optimisation-scaled.jpg";

    useEffect(() => {//hook
        client.current = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" });//Initialisation du client
       // Récupérer l'image de profil de l'utilisateur depuis ton backend
        //const profilePicURL =  fetchUserProfilePicture(user.uid);
      //setprofilePicURL("https://www.bigfootdigital.co.uk/wp-content/uploads/2020/07/image-optimisation-scaled.jpg")//fetchUserProfilePicture(user.uid)
        client.current.on("user-published", handleUserPublished);
        client.current.on("user-unpublished", handleUserUnpublished);

        return () => {
            client.current.off("user-published", handleUserPublished);
            client.current.off("user-unpublished", handleUserUnpublished);
        };
    }, []);

    const join = async () => {
        
        if (joined || !client.current) return; // 🔥 Empêcher de rejoindre plusieurs fois
        axios.get("http://127.0.0.1:8000/Contactes/video_call/get-token/${idCall}")
            .then(response => {
                setToken(response.data.token);
                //setChannelName(response.data.channel_name);
            })
            .catch(error => console.error("Erreur lors de la récupération du token", error));
        try {
            const uid = await client.current.join(APP_ID, CHANNEL, token  || null);//TOKEN
            const audioTrack = isAudioEnabled ? await AgoraRTC.createMicrophoneAudioTrack() : null;
            const videoTrack = isVideoEnabled ? await AgoraRTC.createCameraVideoTrack() : null;
            setLocalTracks({ audioTrack, videoTrack });

            if (videoTrack && localPlayerRef.current) {
                videoTrack.play(localPlayerRef.current);
            }
            console.log(uid)
            console.log(localPlayerRef)
            await client.current.publish([audioTrack, videoTrack].filter(track => track !== null));
            console.log(client.current)
            console.log(client)  // Publier seulement les pistes activées
            setJoined(true);
            console.log(audioTrack)
            console.log(videoTrack)
        } catch (error) {
            console.error("Erreur lors de la connexion :", error);
        }
    };

    const leave = async () => {
        if (!joined || !client.current) return; // 🔥 Empêcher de quitter si pas connecté

        try {
            if (localTracks.videoTrack) localTracks.videoTrack.stop();
            if (localTracks.audioTrack) localTracks.audioTrack.stop();

            await client.current.leave();
            setLocalTracks({ videoTrack: null, audioTrack: null });
            setRemoteUsers({});
            setJoined(false);
            setUserCount(0); // 🔥 Reset du compteur
        } catch (error) {
            console.error("Erreur lors de la déconnexion :", error);
        }
    };

    const handleUserPublished = async (user, mediaType) => {
        /**await client.current.subscribe(user, mediaType);
        setRemoteUsers(prevUsers => {
            const newUsers = { ...prevUsers, [user.uid]: { ...user,hasVideo: isVideoEnabled, hasAudio: isAudioEnabled } };//[user.uid]: user|| DEFAULT_PROFILE_PIC  mediaType === "video" mediaType === "audio"
           // setUserCount(Object.keys(newUsers).length); // 🔥 Mettre à jour le compteur
           console.log(newUsers)
           return newUsers;
        });**/
        // Update the user count: Only increment when a user joins and publishes their media
        /**if (!remoteUsers[user.uid]) {
            setUserCount(prevCount => prevCount + 1); // Increment count when a new user joins
        }
        if (mediaType === "video") {**/
            /*setRemoteUsers(prevUsers => ({
                ...prevUsers,
                [user.uid]: { ...prevUsers[user.uid],hasVideo: mediaType === "video", hasAudio: mediaType === "audio"}//|| DEFAULT_PROFILE_PIC
            }));*/
           /**  const playerContainer = document.createElement("div");
            playerContainer.id = `player-${user.uid}`;
            playerContainer.className = "remote-player w-full h-full bg-black"; // Tailwind classes for styling
            document.getElementById("remote-playerlist").appendChild(playerContainer);
            
            // Lancer la vidéo
            setTimeout(() => {
                user.videoTrack.play(playerContainer);
            }, 100); // Petite attente pour s'assurer que le DOM a le temps de se mettre à jour
        }**/


            await client.current.subscribe(user, mediaType);
            setRemoteUsers(prevUsers => {
                const newUsers = { ...prevUsers, [user.uid]: { ...user, hasVideo: mediaType === "video", hasAudio: mediaType === "audio" } };
                setUserCount(Object.keys(newUsers).length+1);
                return newUsers;
            });
        
            if (mediaType === "video") {
                document.getElementById("remote-playerlist").innerHTML = "";
                const playerContainer = document.createElement("div");
                playerContainer.id = `player-${user.uid}`;
                playerContainer.className = "remote-player w-full h-full bg-black";
                document.getElementById("remote-playerlist").appendChild(playerContainer);
                user.videoTrack.play(playerContainer);
            }

    };

    const handleUserUnpublished = (user, mediaType) => {
        /*setRemoteUsers(prevUsers => {
            const newUsers = { ...prevUsers };
            delete newUsers[user.uid];
            setUserCount(Object.keys(newUsers).length+1); // 🔥 Mettre à jour le compteur
            console.log(newUsers)
            return newUsers;
        });
        

        const playerContainer = document.getElementById(`player-${user.uid}`);
        if (playerContainer && userCount > 1) {
           // playerContainer.remove(); // 🔥 Supprime la vidéo si l'utilisateur part
           // You can either hide or just mark the video/audio track as disabled
           playerContainer.classList.add("hidden"); // Hide the video element if the user disabled the media
           // Alternatively, you can use something like:
           // playerContainer.classList.add("opacity-50"); // To visually show the user has disabled their media
        }else{
            // Update the user count: Decrement only when a user leaves the room
            setUserCount(prevCount => Math.max(prevCount - 1, 0)); // Decrement count only when user leaves
            playerContainer.remove();
        }*/
            setRemoteUsers(prevUsers => {
                const newUsers = { ...prevUsers };
                if (mediaType === "video") {
                    newUsers[user.uid].hasVideo = false;
                } else if (mediaType === "audio") {
                    newUsers[user.uid].hasAudio = false;
                }
                return newUsers;
            });
        
            const playerContainer = document.getElementById(`player-${user.uid}`);
            /*if (playerContainer && mediaType === "video") {
                playerContainer.classList.add("hidden");
            }else{
                playerContainer.classList.remove("hidden");
            }*/
    };

    // Fonctions pour activer/désactiver la caméra et le micro

    //const toggleVideo = () => setIsVideoEnabled(!isVideoEnabled);
    //const toggleAudio = () => setIsAudioEnabled(!isAudioEnabled);
    const toggleVideo = async () => {
        /*setIsVideoEnabled(!isVideoEnabled);
    
        if (isVideoEnabled && localTracks.videoTrack) {
          localTracks.videoTrack.setEnabled(false); // Désactive la vidéo
        } else if (!isVideoEnabled && localTracks.videoTrack) {
          localTracks.videoTrack.setEnabled(true); // Active la vidéo
        }
        // Ensure video track is always published if enabled
       if (localTracks.videoTrack) {
          await client.current.publish([localTracks.videoTrack,localTracks.audioTrack].filter(track => track !== null)); // Only publish video if it's enabled
       }*/
        if (localTracks.videoTrack) {
            if (isVideoEnabled) {
                // Stop and unpublish the video track
                localTracks.videoTrack.stop();
                await client.current.unpublish(localTracks.videoTrack);
            } else {
                // Create and publish a new video track
                const videoTrack = await AgoraRTC.createCameraVideoTrack();
                await client.current.publish(videoTrack);
                videoTrack.play(localPlayerRef.current);
                setLocalTracks(prev => ({ ...prev, videoTrack }));
            }
            setIsVideoEnabled(!isVideoEnabled);
        }
      };
    
      const toggleAudio = async () => {
        /*setIsAudioEnabled(!isAudioEnabled);
    
        if (isAudioEnabled && localTracks.audioTrack) {
          localTracks.audioTrack.setEnabled(false); // Désactive le micro
        } else if (!isAudioEnabled && localTracks.audioTrack) {
          localTracks.audioTrack.setEnabled(true); // Active le micro
        }
         // Ensure audio track is always published if enabled
        if (localTracks.audioTrack) {
          await client.current.publish([localTracks.videoTrack,localTracks.audioTrack].filter(track => track !== null)); // the track is still published, so other users can receive it even if it’s muted.
        }*/
         if (localTracks.audioTrack) {
            if (isAudioEnabled) {
                // Stop and unpublish the audio track
                localTracks.audioTrack.stop();
                await client.current.unpublish(localTracks.audioTrack);
            } else {
                // Create and publish a new audio track
                const audioTrack = await AgoraRTC.createMicrophoneAudioTrack();
                await client.current.publish(audioTrack);
                setLocalTracks(prev => ({ ...prev, audioTrack }));
            }
            setIsAudioEnabled(!isAudioEnabled);
         }
      };
      // Fonction pour récupérer l'image de profil depuis l'API
      /*const fetchUserProfilePicture = async (userId) => {
       try {
        const response = await axios.get(`http://127.0.0.1:8000/api/user/${userId}/profile-picture`);
        return response.data.profilePicture; // Supposons que l’API renvoie { profilePicture: "URL" }
       } catch (error) {
        console.error("Erreur récupération image de profil :", error);
        return DEFAULT_PROFILE_PIC;
      }*/

    return (
        <div className="flex flex-col h-screen items-center inset-shadow-sm inset-shadow-indigo-500 bg-blue-100 relative">
            {/** Background Pattern  
            <div class="absolute inset-0">
                    <div class="relative h-full w-full bg-slate-950 [&>div]:absolute [&>div]:inset-0 [&>div]:bg-[linear-gradient(to_right,#4f4f4f2e_1px,transparent_1px),linear-gradient(to_bottom,#4f4f4f2e_1px,transparent_1px)] [&>div]:bg-[size:14px_24px] [&>div]:[mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]">
                   <div></div>
      
                    </div>
            </div>*/}
            {/* Fond animé avec un gradient <div
                   className="w-screen min-h-screen absolute inset-0 bg-[#010e28] bg-[linear-gradient(to_bottom,_#082740_1px,_transparent_1px),_linear-gradient(to_right,_#082740_1px,_transparent_1px)] [background-size:30px_30px] bg-center overflow-x-hidden animate-bgmove z-0"
            />*/}
             <CosmosNodeNetwork />
            <h3 className="hidden text-xl font-semibold mb-4">Participants dans l'appel : {userCount}</h3>
            {/* Local Player */}
            {/*<div id="local-player" className="w-72 h-48 bg-gray-800" ref={localPlayerRef}></div>*/}

            {/* Remote Players */}
            {/*<div id="remote-playerlist" className="flex flex-wrap justify-center gap-4 mt-4"></div>*/}
            {/* Zone vidéo w-full h-full flex*/}
          <div className="p-4 flex w-full h-full flex-col items-center justify-center absolute z-10">
             <div className="rounded-xl relative h-full min-w-lg w-5/6 justify-center items-center overflow-hidden">
                {/* Utilisateur distant <div id="remote-playerlist" border border-white className={` w-full h-full ${userCount > 0 ? "z-0" : "z-10"}`}></div>*/}
                
                <div 
                    id="local-player" 
                    ref={localPlayerRef} 
                    className={`bg-black rounded-lg border-4 border-gray-700 absolute transition-all duration-300 ${
                        userCount > 0 
                        ? "top-4 left-4 w-64 h-1/3 z-20"// w-40 h-28
                        :"w-full h-full z-10 object-cover" // w-9/10 h-9/10w-full h-full
                    }`}
                >
                    {/* Afficher l'image de profil si la vidéo est désactivée*/ }
                    {!isVideoEnabled && (
                        <img 
                            src={DEFAULT_PROFILE_PIC} 
                            alt="Profile" 
                            className="w-full h-full object-cover rounded-lg" 
                        />
                    )}
                </div>
                {/*ref={remotePlayerRef}  Utilisateur local w-2/3 h-2/3 w-full h-full*/}
                <div id="remote-playerlist" className={`w-9/10 h-full border-2 border-gray-700 ${userCount > 0 ? "z-0" : "z-10"}`}>
                          {!Object.values(remoteUsers).hasVideo && userCount <=0  ? null : (
                            <img 
                              src={DEFAULT_PROFILE_PIC} 
                              alt="Profile" 
                              className="w-full h-full object-cover rounded-lg" //w-full h-full
                             />
                          )}
                </div>
               
            </div>
            {/* Buttons */}
            <div id="buttons_controles" className="p-4 absolute flex flex-wrap items-center justify-center gap-4 z-20 inset-x-0 bottom-4">  
              <div className="flex items-center justify-center">
                <button 
                    onClick={join} 
                    className={`p-4 text-white rounded-full disabled:bg-gray-400  flex items-center justify-center bg-green-500 shadow-lg shadow-green-500/50 
                              ${ joined ? "cursor-not-allowed hidden" : "" 
                                   }
                                 `} //bg-blue-500// bg-linear-to-r/decreasing from-indigo-500 to-teal-400
                    disabled={joined}
                >
                    <FaPhoneAlt className="h-5 w-5"/>
                    {/**Join**/}
                </button>
                <button 
                    onClick={leave} 
                    className={`bg-red-500 shadow-lg shadow-red-500/50 ml-2 p-4 bg-red-500 text-white rounded-full disabled:bg-gray-400  flex items-center justify-center
                              ${ !joined ? "cursor-not-allowed hidden" : "" }
                           `}
                    disabled={!joined}
                >
                    <FaPhoneAlt className="h-5 w-5" />
                   {/** Leave*/} 
                </button>
              </div>
              {/* mb-4 Contrôles de la caméra et du micro */}
              <div className=" flex flex-wrap items-center justify-center gap-4">
                <button
                    onClick={toggleVideo}
                    className={`p-4 ${isVideoEnabled ? 'bg-blue-500 shadow-lg shadow-blue-500/50 ' : 'bg-blue-100'} text-white rounded-full  justify-center flex items-center`}
                >
                    {isVideoEnabled ? (
                        <FaVideo  className="h-5 w-5 " />
                    ) : (
                        <FaVideoSlash className="h-5 w-5 " />
                    )}
                    {/*isVideoEnabled ? 'Turn off Camera' : 'Turn on Camera'*/}
                </button>
                <button
                    onClick={toggleAudio}
                    className={`p-4 ${isAudioEnabled ? 'bg-blue-500 shadow-lg shadow-blue-500/50 ' : 'bg-blue-100'} text-white rounded-full flex items-center`}
                >
                    {isAudioEnabled ? (
                        <FaMicrophone className="h-5 w-5" />
                    ) : (
                        <FaMicrophoneSlash className="h-5 w-5" />
                    )}
                    {/*isAudioEnabled ? 'Mute Mic' : 'Unmute Mic'*/}
                </button>
              </div>
            </div>
          </div>
        </div>
    );
};
/** <div id="local-player" className="local-player">
                {joined && localTracks.videoTrack && <video autoPlay playsInline ref={el => el && localTracks.videoTrack.play(el)} />}
            </div>
                     
            */
export default VideoCall;
