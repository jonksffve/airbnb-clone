import { Select, Space } from 'antd';
import { getAll } from '../../../hooks/WorldCountries';

const CountrySelect = ({ onSelect, value }) => {
	const countries = getAll();
	const { Option } = Select;

	return (
		<Select
			placeholder='Select anywhere in the world!'
			showSearch
			value={value}
			onChange={(value) => {
				onSelect(value);
			}}
			allowClear
		>
			{countries.map((country) => (
				<Option
					key={country.label}
					value={country.value}
					label={country.label}
				>
					<Space className='flex flex-row items-center gap-3'>
						<span role='img'>{country.flag}</span>
						{country.label}-
						<span className='text-neutral-500'>{country.region}</span>
					</Space>
				</Option>
			))}
		</Select>
	);
};

export default CountrySelect;
