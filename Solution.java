import java.util.*;
public class Solution {
    // hashmap to store braille translations 
    static HashMap<Character,String> map=new HashMap<Character,String>();
    //static initialization block
    static{
        map.put('a',"100000");
    	map.put('b',"110000");
    	map.put('c',"100100");
    	map.put('d',"100110");
    	map.put('e',"100010");
    	map.put('f',"110100");
    	map.put('g',"110110");
    	map.put('h',"110010");
    	map.put('i',"010100");
    	map.put('j',"010110");
    	map.put('k',"101000");
    	map.put('l',"111000");
    	map.put('m',"101100");
    	map.put('n',"101110");
    	map.put('o',"101010");
    	map.put('p',"111100");
    	map.put('q',"111110");
    	map.put('r',"111010");
    	map.put('s',"011010");
    	map.put('t',"011110");
    	map.put('u',"101001");
    	map.put('v',"111001");
    	map.put('w',"010111");
    	map.put('x',"101101");
    	map.put('y',"101111");
    	map.put('z',"101011");
    	map.put(' ',"000000");
    	map.put('A',"000001");
    }
    public static void main(String[] args){
        System.out.print(solution("The quick brown fox jumps over the lazy dog").equals("000001011110110010100010000000111110101001010100100100101000000000"));
    }
    public static String solution(String s) {
    	// Your code here
    	HashMap<Character,String> map=new HashMap<Character,String>();
    	map.put('a',"100000");
    	map.put('b',"110000");
    	map.put('c',"100100");
    	map.put('d',"100110");
    	map.put('e',"100010");
    	map.put('f',"110100");
    	map.put('g',"110110");
    	map.put('h',"110010");
    	map.put('i',"010100");
    	map.put('j',"010110");
    	map.put('k',"101000");
    	map.put('l',"111000");
    	map.put('m',"101100");
    	map.put('n',"101110");
    	map.put('o',"101010");
    	map.put('p',"111100");
    	map.put('q',"111110");
    	map.put('r',"111010");
    	map.put('s',"011010");
    	map.put('t',"011110");
    	map.put('u',"101001");
    	map.put('v',"111001");
    	map.put('w',"010111");
    	map.put('x',"101101");
    	map.put('y',"101111");
    	map.put('z',"101011");
    	map.put(' ',"000000");
    	map.put('A',"000001");
    	StringBuilder res = new StringBuilder();
    	
    	for(int i=0;i<s.length();i++){
    	    char ch=s.charAt(i);
    	    if(Character.isUpperCase(ch)){
    	        res.append(map.get('A'));
    	    }
    	    ch=Character.toLowerCase(ch);
    	    res.append(map.get(ch));
    	}
    	//System.out.println(res);
    	return res.toString();
    }
}