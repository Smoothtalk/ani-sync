import React, { useState, createContext, useEffect } from "react";
const UserContext = createContext("Guest");

function UserProvider({ children }) {
  const storedUser = localStorage.getItem("user");
  const [user, setUser] = useState(storedUser || "");

  useEffect(() => {
    localStorage.setItem("user", user);
  }, [user]);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
}

export { UserProvider, UserContext };
