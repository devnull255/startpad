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
	
	public interface Trace
		{
		public void Callback(String trace);
		}
	
	private Trace trace; 
	
	static Rotor[] rotors =
		{
		new Rotor("I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q'),
		new Rotor("II", "AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E'),
		new Rotor("III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V'),
		new Rotor("IV", "ESOVPZJAYQUIRHXLNFTGKDCMWB", 'J'),
		new Rotor("V", "VZBRGITYUPSDNHLXAWMJQOFECK", 'Z'),
		new Rotor("B", "YRUHQSLDPXNGOKMIEBFZCWVJAT", ' '),
		new Rotor("C", "FVPJIAOYEDRZXWGCTKUQSBNMHL", ' ')
		};
	
	public Enigma(Trace trace)
		{
		this.trace = trace;
		
		if (this.trace != null)
			this.trace.Callback("Constructed");
		}

	public static void main(String[] args)
		{
			System.out.println("Hello, world");
			for (int i = 0; i < rotors.length; i++)
				System.out.println(rotors[i].name + ": " + rotors[i].wires + "(" +
					rotors[i].notch + ")");

			Enigma e = new Enigma(new Trace()
				{
				@Override
				public void Callback(String trace)
					{
						System.out.println("Trace: " + trace);
					}
			});
			
			if (e.trace != null)
				{
				System.out.println("has trace");
				}
			else
				{
				System.out.println("no trace");
				}
		}

}

