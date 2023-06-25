import AvatarImg from '../../src/assets/images/placeholder.jpg';

const Avatar = () => {
	return (
		<img
			className='rounded-full'
			src={AvatarImg}
			alt=''
			height={30}
			width={30}
		/>
	);
};

export default Avatar;
