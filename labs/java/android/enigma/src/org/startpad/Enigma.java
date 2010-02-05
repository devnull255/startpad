/*
  Enigma.java - Enigma machine simulation.

  Ported from Enigma.js, Feb, 2010

  References:
   	  Paper Enigma - http://mckoss.com/Crypto/Enigma.htm
   	  Enigma Simulator - http://bit.ly/enigma-machine
   	  Enigma History - http://en.wikipedia.org/wiki/Enigma_machine


 */

package org.startpad;

public class Enigma
{
	static class Rotor
	{
		String name;
		String wires;
		char notch;
		
		public Rotor() {}
		
		public Rotor(String name, String wires, char notch)
			{
			this.name = name;
			this.wires = wires;
			this.notch = notch;
			}
	}
	
	static Rotor[] rotors =
		{
		new Rotor("I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q'),
		new Rotor("II", "AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E'),
		new Rotor("III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V'),
		new Rotor("IV", "ESOVPZJAYQUIRHXLNFTGKDCMWB", 'J'),
		new Rotor("V", "VZBRGITYUPSDNHLXAWMJQOFECK", 'Z')
		};

	public static void main(String[] args)
		{
			System.out.println("Hello, world");
			for (int i = 0; i < rotors.length; i++)
				System.out.println(rotors[i].name + ": " + rotors[i].wires + "(" +
					rotors[i].notch + ")");
		}

}

