const CategoryInput = ({ selected, label, icon: Icon, onClick }) => {
	return (
		<div
			className={`flex
            cursor-pointer
            flex-col
            gap-3
            rounded-xl
            border-2
            p-4
            transition
            hover:border-black
            ${selected ? 'border-black' : 'border-neutral-200'}
            `}
			onClick={() => {
				onClick(label);
			}}
		>
			<Icon size={30} />
			<div className='font-semibold'>{label}</div>
		</div>
	);
};

export default CategoryInput;
