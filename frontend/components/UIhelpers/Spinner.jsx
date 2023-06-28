import { Spin } from 'antd';

const Spinner = () => {
	return (
		<Spin
			tip='Sending data'
			size='large'
		>
			<div className='content h-[35vh]' />
		</Spin>
	);
};

export default Spinner;
