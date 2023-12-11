
import React from 'react';
import newLogo from '../assets/SER-2.png';
function Header() {
    return (
    <header className="App-header">
        <img src={newLogo} alt="Logo" />
        {/* Ajoutez d'autres éléments de navigation ou marque si nécessaire */}
    </header>
    );
}

export default Header;
