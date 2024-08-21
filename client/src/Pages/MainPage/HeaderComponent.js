const Header = () => {
  return (
    <div className="header bg-gray-100 p-4 flex justify-between items-center">
      <h1 className="text-xl font-bold">Appointment Dashboard</h1>
      <input
        type="text"
        placeholder="Search..."
        className="border p-2 rounded-lg"
      />
      <div className="user-info flex items-center">
        <span>Dr. Jackson</span>
        <img
          src="https://via.placeholder.com/40"
          alt="Profile"
          className="rounded-full w-10 h-10 ml-4"
        />
      </div>
    </div>
  );
};

export default Header;