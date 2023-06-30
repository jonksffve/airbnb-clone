import { AiFillHeart, AiOutlineHeart } from 'react-icons/ai';
import { favoriteAPI } from '../../api/AuthAPI';
import { useEffect, useState } from 'react';

const HeartButton = ({ liked, listingID, token }) => {
	const [likeState, setLikeState] = useState(false);

	useEffect(() => {
		setLikeState(liked);
	}, [liked]);

	const handleLike = () => {
		favoriteAPI(listingID, token, likeState, setLikeState);
	};

	return (
		<div
			className='relative cursor-pointer transition hover:opacity-80'
			onClick={handleLike}
		>
			<AiOutlineHeart
				size={28}
				className='absolute -right-[2px] -top-[2px] fill-neutral-300'
			/>
			<AiFillHeart
				size={24}
				className={likeState ? 'fill-rose-500' : 'fill-neutral-500/70'}
			/>
		</div>
	);
};

export default HeartButton;
