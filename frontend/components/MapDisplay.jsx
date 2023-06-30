import { MapContainer, TileLayer, Marker, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const MapDisplay = ({ center }) => {
	const UpdateCenter = ({ center }) => {
		const map = useMap();
		map.setView(center, map.getZoom());
		return null;
	};

	return (
		<MapContainer
			center={center || [51.505, -0.09]}
			zoom={10}
			scrollWheelZoom={false}
			className='h-[35vh] rounded-lg'
		>
			<TileLayer
				attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
				url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
			/>
			<Marker position={center || [51.505, -0.09]} />
			<UpdateCenter center={center || [51.505, -0.09]} />
		</MapContainer>
	);
};

export default MapDisplay;
