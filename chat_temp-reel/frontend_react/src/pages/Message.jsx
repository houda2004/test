import React from 'react';

function Message({ sender, timestamp, content, isCurrentUser }) {//,fileName,audioData
    return (
        <div className={`p-3 mb-3 max-w-[80%] flex items-end space-x-2`}>
            <img src="https://www.bigfootdigital.co.uk/wp-content/uploads/2020/07/image-optimisation-scaled.jpg" alt="User" 
            class={`w-8 h-8 rounded-full  ${
                isCurrentUser
                 ? 'order-last'// Styles pour l'utilisateur actuel
                 : '' // Styles pour les autres utilisateurs'
               }`}></img>
                 
            <div>
                <p><strong className= 'text-gray-500 self-start' >{sender}</strong></p>              
                 <div class={`border rounded-lg p-3 ${
                      isCurrentUser
                       ? 'bg-blue-400 text-white'// Styles pour l'utilisateur actuel'bg-purple-100 text-white'
                       : 'bg-blue-100 ' // Styles pour les autres utilisateurs'bg-azure-100 text-black '
                     }
                 `}>
                    <p>{content}</p>
                    <span class={`text-xs  ${
                      isCurrentUser
                       ? 'text-gray-100'// Styles pour l'utilisateur actuel'bg-purple-100 text-white'
                       : 'text-gray-500' // Styles pour les autres utilisateurs'bg-azure-100 text-black '
                     }`}><strong> {timestamp}</strong></span>
                 </div>
            </div>
        </div>
    );
}

export default Message;
