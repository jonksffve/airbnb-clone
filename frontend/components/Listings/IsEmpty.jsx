import Heading from '../Modals/Heading';
import Button from '../UIhelpers/Buttons/Button';

const IsEmpty = ({ onClick = undefined, showReset = undefined }) => {
	return (
		<div className='flex h-[60vh] flex-col items-center justify-center gap-2'>
			<Heading
				title='Data not found.'
				subtitle='We have not found any listing that matches this search.'
				center
			/>
			<div className='mt-4 w-48'>
				{showReset && (
					<Button
						outline
						label='Reset'
						onClick={onClick}
					/>
				)}
			</div>
		</div>
	);
};

export default IsEmpty;
