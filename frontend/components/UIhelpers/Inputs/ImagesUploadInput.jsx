import { BiImageAdd } from 'react-icons/bi';

const ImagesUploadInput = ({ value, onChange }) => {
	return (
		<div className='flex h-[35vh] flex-row items-center justify-center border-2 border-dashed'>
			<div className='w-100 h-100 flex flex-col items-center justify-center'>
				<label
					htmlFor='images'
					className='cursor-pointer'
				>
					<BiImageAdd size={40} />
				</label>
				<p>{value ? value.name : 'Select image to upload'}</p>
			</div>
			<input
				onChange={(event) => {
					onChange(event.target.files[0]);
				}}
				hidden
				type='file'
				name='images'
				id='images'
			/>
		</div>
	);
};

export default ImagesUploadInput;
