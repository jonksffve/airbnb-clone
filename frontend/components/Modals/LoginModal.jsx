import { useState } from 'react';
import Modal from '../UIhelpers/Modal';
import { useDispatch, useSelector } from 'react-redux';
import { uiActions } from '../../store/ui-slice';

const LoginModal = () => {
	const uiState = useSelector((state) => state.ui);
	const dispatch = useDispatch();
	const [isLoading, setIsLoading] = useState(false);

	const handleClose = () => {
		dispatch(uiActions.closeLoginModal());
	};

	return (
		<Modal
			isOpen={uiState.showLoginModal}
			onClose={handleClose}
			title='User authentication'
		/>
	);
};

export default LoginModal;
