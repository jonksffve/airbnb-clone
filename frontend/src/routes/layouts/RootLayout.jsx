import { Fragment } from 'react';
import { Outlet } from 'react-router-dom';
import MainNavigation from '../../../components/Menu/Navbar';
import Modal from '../../../components/Modals/Modal';

const RootLayout = () => {
  return (
    <Fragment>
      <MainNavigation />
      <main>
        <Outlet />
      </main>
      <Modal
        isOpen
        title='Login'
        actionLabel='Submit'
      />
    </Fragment>
  );
};

export default RootLayout;
