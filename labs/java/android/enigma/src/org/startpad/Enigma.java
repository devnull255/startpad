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
		int[] map = new int[26];
		int[] mapReverse = new int[26];
		
		public Rotor() {}
		
		public Rotor(String name, String wires, char notch)
			{
			this.name = name;
			this.wires = wires;
			this.notch = notch;
			
			this.CreateMapping();
			}
		
		private void CreateMapping()
			{
			for (int iFrom = 0; iFrom < 26; iFrom++)
				{
				int iTo = iFromCh(this.wires.charAt(iFrom));
				this.map[iFrom] = (26 + iTo - iFrom) % 26;
				this.mapReverse[iTo] = (26 + iFrom - iTo) % 26;
				}
			}
		}
	
	static class Settings
		{
		String[] rotors;
		String reflector;
		char[] position;
		char[] rings;
		String plugs;
		}
	
	public interface Trace
		{
		public void Callback(String trace);
		}
	
	private Trace trace; 
	
	static Rotor[] rotorsBox =
		{
		new Rotor("I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q'),
		new Rotor("II", "AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E'),
		new Rotor("III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V'),
		new Rotor("IV", "ESOVPZJAYQUIRHXLNFTGKDCMWB", 'J'),
		new Rotor("V", "VZBRGITYUPSDNHLXAWMJQOFECK", 'Z'),
		new Rotor("B", "YRUHQSLDPXNGOKMIEBFZCWVJAT", ' '),
		new Rotor("C", "FVPJIAOYEDRZXWGCTKUQSBNMHL", ' ')
		};
	
	// Instance variables
	
	Settings settings;
	Rotor[] rotors = new Rotor[3];
	Rotor reflector;
	int[] position = new int[3];
	
	public Enigma(Trace trace)
		{
		this.trace = trace;
		
		if (this.trace != null)
			this.trace.Callback("Constructed");
		
		// Default settings
		Settings settings = new Settings();
		
		settings.rotors = new String[] {"I", "II", "III"};
		settings.reflector = "B";
		settings.position = new char[] {'M', 'C', 'K'};
		settings.rings = new char[] {'A', 'A', 'A'};
		settings.plugs = "";
		init(settings);
		}
	
	public void init(Settings settings)
		{
		if (settings != null)
			this.settings = settings;
		
		for (int i = 0; i < 3; i++)
			this.rotors[i] = rotorFromName(this.settings.rotors[i]);
		
		this.reflector = rotorFromName(this.settings.reflector);
		
		for (int i = 0; i < 3; i++)
			this.position[i] = iFromCh(this.settings.position[i]);
		}
	
	private Rotor rotorFromName(String name)
		{
		for (int i = 0; i < rotorsBox.length; i++)
			if (name == rotorsBox[i].name)
				return rotorsBox[i];
		return null;
		}
	
	private static int iFromCh(char ch)
		{
		ch = Character.toUpperCase(ch);
		return ch - 'A';
		}
	
	private static char chFromI(int i)
		{
		return (char) ((int) 'A' + i);
		}
	
	public static String groupLetters(String s)
		{
		s = s.toUpperCase();
		s = s.replaceAll("[^A-Z]", "");
		return groupBy(s, 5, ' ');
		}
	
	public static String groupBy(String s, int n, char c)
		{
		String sOut = "";
		String sSep = "";
		while (s.length() > n)
			{
			sOut += sSep + s.substring(0, n);
			s = s.substring(n);
			sSep = " ";
			}
		if (s.length() > 0)
			sOut += sSep + s;
		return sOut;
		}
		
	public static void main(String[] args)
		{
			System.out.println("Hello, world");
			for (int i = 0; i < rotorsBox.length; i++)
				System.out.println(rotorsBox[i].name + ": " + rotorsBox[i].wires + "(" +
					rotorsBox[i].notch + ")");

			Enigma e = new Enigma(new Trace()
				{
				@Override
				public void Callback(String trace)
					{
						System.out.println("Trace: " + trace);
					}
			});
			
			System.out.println('Z' - 'A');
			
			if (e.trace != null)
				{
				System.out.println("has trace");
				}
			else
				{
				System.out.println("no trace");
				}
			
			System.out.println(groupBy("abcdefghijklmnop", 5, ' '));
		}

}

