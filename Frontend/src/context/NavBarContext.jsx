import React, { useState, createContext, useEffect } from "react";
const NavBarContext = createContext(false);

function NavBarProvider({ children }) {
  const [navBarOpen, setNavBarOpen] = useState(false);

  //   useEffect(() => {}, [navBarOpen]);

  return (
    <NavBarContext.Provider value={{ navBarOpen, setNavBarOpen }}>
      {children}
    </NavBarContext.Provider>
  );
}

export { NavBarProvider, NavBarContext };
