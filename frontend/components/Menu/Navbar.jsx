import Container from '../UIhelpers/Container';
import Categories from './Categories';
import Logo from './Logo';
import Search from './Search';
import UserMenu from './UserMenu';

const Navbar = () => {
	return (
		<nav className='w-full bg-white shadow-sm'>
			<div className='border-b-[1px] py-4'>
				<Container>
					<div className='flex flex-row items-center justify-between gap-3 md:gap-0'>
						<Logo />
						<Search />
						<UserMenu />
					</div>
				</Container>
			</div>
			<Categories />
		</nav>
	);
};

export default Navbar;
