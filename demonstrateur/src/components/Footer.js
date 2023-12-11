// Dans src/components/Footer.js

import React from 'react';
import newLogo from '../assets/Logo_Efrei.png';


function Footer() {
  return (
    <footer className="App-footer">
      <img src={newLogo} alt="Logo" />
        <ul>
        <li>Participants:</li>
        <li>Yao Anicet AGBONON EDAGBEDJI</li>
        <li>Maroua BOUDOUKHA</li> 
        <li>Lise CICERON</li>
        <li>Sophie Manuella SIAKE TCHOUAMOU</li>
        <li>Frederique WANDJI K </li>
        <li>Yvan Gavinetto MELI MANFOUO</li>
        </ul>
    </footer>
  );
}

export default Footer;
