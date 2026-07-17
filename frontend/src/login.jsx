import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Login() {

  const handleGoogleLogin = () => {
    window.location.href = "http://localhost:8000/auth/google/login";
  };

  return (
    <div className="login-container">
    
        <h2>Login</h2>

        <button onClick={handleGoogleLogin}>Continue with Google</button>
    
    </div>
  );
}

export default Login;
