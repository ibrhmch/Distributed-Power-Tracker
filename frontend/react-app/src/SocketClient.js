import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import MapView from './MapView';

const mapCenter = [40.007259752621174, -105.26350055410776]

const App = () => {
    const [socket, setSocket] = useState(null);
    const [dataPoints, setDataPoints] = useState({});

    useEffect(() => {
        // Define the Socket.IO server URL
        // const serverUrl = '/frontend/socket';
        // const newSocket = io(serverUrl, { path: '/frontend/socket/connect/socket.io', transports: ['websocket'] });

        const newSocket = io('http://socket:5001', { transports: ['websocket'] });

        setSocket(newSocket);

        newSocket.on('NewPanelData', (data) => {
            console.log(data);

            setDataPoints(prevDataPoints => {
                const newDataPoints = { ...prevDataPoints };
                newDataPoints[data.panelId] = { ...prevDataPoints[data.panelId], powerKw: data.powerKw }

                return newDataPoints;
            });

        });

        fetch('/frontend/get_panels')
            .then(response => response.json())
            .then(data => {
                setDataPoints({ ...data });
            })
            .catch(error => console.error('Error fetching data:', error));

        return () => newSocket.close();
    }, []);

    if (Object.keys(dataPoints).length > 0) {
        console.log(dataPoints);
    }

    return (
        <div>
            <div className='flex justify-center items-center w-full py-8 my-2 bg-gray-500 text-white' >
                <h1 className="text-center text-3xl font-normal italic">Solar Panel Data Visualizer</h1>
            </div>

            <div className="flex justify-center items-center w-screen">
                <div className="flex justify-center items-center w-2/5">
                    <div className='flex-col justify-center items-center w-4/5'>
                        {Object.keys(dataPoints).map(panelId => (
                            <div className='p-2 my-1 font-normal bg-gray-500 text-white rounded-md' key={panelId}>
                                <p>Name: {dataPoints[panelId].name}</p>
                                <p>Power: {dataPoints[panelId].powerKw}</p>
                            </div>
                        ))}
                    </div>
                </div>

                <div className='flex items-center justify-center' style={{ height: '70vh' }}>
                    <div className="border-l border-gray-400 bg-black h-3/4"></div>
                </div>
                <div className='w-3/4'>
                    <MapView dataPoints={dataPoints} />
                </div>
            </div>
        </div>
    );
};

export default App;
