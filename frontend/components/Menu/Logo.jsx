import LogoImg from '../../src/assets/images/logo.png';

const Logo = () => {
	return (
		<img
			className='hidden cursor-pointer md:block'
			src={LogoImg}
			alt='Logo'
			height={100}
			width={100}
		/>
	);
};

export default Logo;
