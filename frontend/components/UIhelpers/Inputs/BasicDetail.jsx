import { useCallback } from 'react';
import { AiOutlineMinus, AiOutlinePlus } from 'react-icons/ai';

const BasicDetail = ({ title, subtitle, value, onChange }) => {
	const addHandler = useCallback(() => {
		onChange(+value + 1);
	}, [onChange, value]);

	const removeHandler = useCallback(() => {
		if (value === 1) return;
		onChange(+value - 1);
	}, [onChange, value]);

	return (
		<div className='flex flex-row items-center justify-between'>
			<div className='flex flex-col'>
				<div className='font-medium'>{title}</div>
				<div className='font-light text-gray-600'>{subtitle}</div>
			</div>

			<div className='flex flex-row items-center gap-4'>
				<div
					onClick={removeHandler}
					className={`flex 
                    h-10 
                    w-10 
                    items-center 
                    justify-center
                    rounded-full
                    border-[1px]
                    border-neutral-400
                    text-neutral-600
                    transition
                    hover:opacity-80
                    ${value === 1 ? 'cursor-not-allowed' : 'cursor-pointer'}`}
				>
					<AiOutlineMinus />
				</div>
				<div className='text-lx font-light text-neutral-600'>{value}</div>
				<div
					onClick={addHandler}
					className='flex 
                            h-10 
                            w-10 
                            cursor-pointer 
                            items-center 
                            justify-center
                            rounded-full
                            border-[1px]
                            border-neutral-400
                            text-neutral-600
                            transition
                            hover:opacity-80
                            '
				>
					<AiOutlinePlus />
				</div>
			</div>
		</div>
	);
};

export default BasicDetail;
