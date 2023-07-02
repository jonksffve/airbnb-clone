import { Spin } from 'antd';

const Spinner = () => {
	return (
		<Spin
			tip='LOADING'
			size='large'
			className='hover:cursor-not-allowed'
		>
			<div className='content h-[40vh]' />
		</Spin>
	);
};

export default Spinner;
