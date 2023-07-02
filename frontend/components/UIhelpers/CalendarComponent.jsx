import { DateRange } from 'react-date-range';
import 'react-date-range/dist/styles.css'; // main style file
import 'react-date-range/dist/theme/default.css'; // theme css file
import Spinner from './Spinner';

const CalendarComponent = ({ disabled, value, onChange, disabledDates }) => {
	if (disabled) {
		return <Spinner />;
	}
	return (
		<DateRange
			rangeColors={['#262626']}
			ranges={[value]}
			onChange={onChange}
			date={new Date()}
			direction='vertical'
			showDateDisplay={false}
			minDate={new Date()}
			disabledDates={disabledDates}
		/>
	);
};

export default CalendarComponent;
