import React, { useContext, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";

export default function Login() {
  const navigate = useNavigate();
  const [value, setValue] = useState(""); //input field updating methods
  const { setUser } = useContext(UserContext); //get user from context

  function handleSubmit(e) {
    e.preventDefault();
    setUser(value);
    navigate("/recent");
  }
  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
        ></input>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}
