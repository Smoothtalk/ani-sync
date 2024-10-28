import React, { useState } from "react";
import { createContext } from "react";
const UserContext = createContext("Guest");

function UserProvider({ children }) {
  const [user, setUser] = useState("");
  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
}

export { UserProvider, UserContext };
