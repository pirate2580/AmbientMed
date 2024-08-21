import logo from '../../assets/ambientmed.png'

const Sidebar = () => {
  return (
    <div className="sidebar bg-gray-200 p-4 w-1/6 h-screen">
      <div className="profile-pic mb-4">
        <img
          src={logo}
          alt="Profile"
          className="rounded-full w-25 h-24 mx-auto"
        />
        <p className="text-center mt-2">Dr. Jackson</p>
      </div>
      <div className="nav-icons flex flex-col items-center">
        <div className="icon mb-4">
          <span role="img" aria-label="icon">🏠</span>
        </div>
        <div className="icon mb-4">
          <span role="img" aria-label="icon">📅</span>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;