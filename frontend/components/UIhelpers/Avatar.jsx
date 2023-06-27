import AvatarImg from '../../src/assets/images/placeholder.jpg';

const Avatar = ({ avatar }) => {
	return (
		<img
			className='rounded-full'
			src={avatar || AvatarImg}
			alt=''
			height={30}
			width={30}
		/>
	);
};

export default Avatar;
