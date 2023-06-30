import { Link } from 'react-router-dom';
import LogoImg from '../../src/assets/images/logo.png';

const Logo = () => {
	return (
		<Link to={'/'}>
			<img
				className='hidden cursor-pointer md:block'
				src={LogoImg}
				alt='Logo'
				height={100}
				width={100}
			/>
		</Link>
	);
};

export default Logo;
