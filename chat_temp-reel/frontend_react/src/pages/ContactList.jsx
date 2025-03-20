import React from 'react';
/*  rooms_with_other_user = [
        {'id': room.id, 'other_user': room.get_autre_user_room(person_current).user_compte.first_name} for room in rooms
    ] */
const ContactList = ({ rooms, onRoomSelect }) => {// affiche la liste des contacte de user corant 
return (
    <div className="overflow-y-auto  overflow-hidden">{/** bg-white shadow-md rounded-lg*/}
        {/* En-tête de la carte 
         <div className="bg-gray-100 p-4 border-b border-gray-200">
            <h5 className="text-lg font-semibold">Contacts</h5>
        </div>

        */}
        {/* Liste des contacts */}
        <div className="p-2 ">
            <ul className="space-y-2">
                {rooms.map((room, index) => (
                    <li key={index} className="flex items-end space-x-2 p-3 hover:bg-gray-200 rounded rounded-lg transition-colors cursor-pointer">
                      <div  onClick={() => onRoomSelect(room.id)} >
                        <img src="https://www.bigfootdigital.co.uk/wp-content/uploads/2020/07/image-optimisation-scaled.jpg"  alt="User" class={`w-8 h-8 rounded-full`}></img>             
                        <p className="flex justify-between items-center text-gray-700">
                            Room {room.other_user}
                        </p>
                      </div>  
                    </li>
                ))}
            </ul>
        </div>
    </div>
    );
};

export default ContactList;
/** <div className="Contactes card">
            <div className="card-header">
                <h5>Contacts</h5>
            </div>
            <div className="Contactes_liste card-body">
                <ul className="list-group">
                    {rooms.map((room, index) => (
                        <li key={index} className="list-group-item">
                            <p onClick={() => onRoomSelect(room.id)} clpssName="d-flex justify-content-between align-items-center">
                               Room {room.other_user}
                            </p>
                        </li>
                    ))}
                </ul>
            </div>
        </div>*/