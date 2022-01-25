#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <vector>
#define MAXBITS 100000
#include "comp.h"


                                                                                                                                                                                                                             
class bitC {
	public:
		bitC();
		int	addChar(char c);
		int getBitA() {return bp;};		// returns current bit address
		int64_t	getValue(int n);	// returns the value in decimal of the binary number of the current bit thru n bits
								// the current bit pointer is moved accordingly
		int setBitReturn(int n) { br = bp + n; return br; };
		void out();
	private:
		void addbits(int b1, int b2, int b3, int b4);
		int	bits[MAXBITS];  // 0, 1 (or -1 to indicate invalid bit)
		int nbits;
		int bp;		// index into current place in bits
		int br;		// br represents 
};

bitC::bitC()
{
	nbits = 0;
	bp = 0;
	br = 0;
	for (int i = 0; i < MAXBITS; i++) bits[i] = -1;
}

void bitC::out()
{
	for (int i = 0; i < MAXBITS; i++)
	{
		if (bits[i] == -1) break;
		printf("%2d", bits[i]);
		if ((i + 1)/ 40 * 40 == i + 1) printf("\n");
	}
	printf("\n");
}


int64_t	bitC::getValue(int n)	// returns the value in decimal of the binary number of the current bit thru n bits
{

	int64_t sum = 0;

	for (; n > 0; n--)
	{
		sum = sum * 2 + bits[bp];
		bp++;
	}
	return sum;
}


void bitC::addbits(int b1, int b2, int b3, int b4)
{
	bits[nbits++] = b1;
	bits[nbits++] = b2;
	bits[nbits++] = b3;
	bits[nbits++] = b4;
}

int	bitC::addChar(char c)
{
	switch(c)
	{
		case '0': addbits(0,0,0,0); break;
		case '1': addbits(0,0,0,1); break;
		case '2': addbits(0,0,1,0); break;
		case '3': addbits(0,0,1,1); break;
		case '4': addbits(0,1,0,0); break;
		case '5': addbits(0,1,0,1); break;
		case '6': addbits(0,1,1,0); break;
		case '7': addbits(0,1,1,1); break;
		case '8': addbits(1,0,0,0); break;
		case '9': addbits(1,0,0,1); break;
		case 'A': addbits(1,0,1,0); break;
		case 'B': addbits(1,0,1,1); break;
		case 'C': addbits(1,1,0,0); break;
		case 'D': addbits(1,1,0,1); break;
		case 'E': addbits(1,1,1,0); break;
		case 'F': addbits(1,1,1,1); break;
		default: return -1;
	}
	return nbits;
}
int processPacket(comp &cmp, bitC &b);

int	sum_version = 0;
int	oper_count = 0;
int	eop_count = 0;

int64_t  processLiteral(comp &cmp, bitC &b)
{
	bool done = false;
	int64_t  litval = 0;
	//int  p16 = 1;
	while (!done)
	{
		// get next five bits - if bit '4' is clear, - value is done
		// otherwise, need to get next one
		int64_t	fiveb = b.getValue(5);
		if (fiveb <= 15)
			done = true;
		else
			fiveb -= 16;	// get rid of the leading bit
		litval = 16 * litval + fiveb;
	}
	//printf("%ld\n", litval);
	cmp.push(opobj(litval, LITERAL));
	return litval;
}

int	processOperand(comp &cmp, op_type t, bitC &b)
{
	int ltype = b.getValue(1);
	int sb = b.getBitA();
	int	total_bits = 0;
	int total_packets = 0;
	cmp.push(opobj(0, t));
	oper_count++;

	if (ltype == 0)
	{
		total_bits = b.getValue(15);
		//printf("--processOperand:: Total Bits = %d\n", total_bits);
		int start = b.getBitA();
		int end = start + total_bits;
		while (end > b.getBitA())
		{
			processPacket(cmp, b);
		}
		//printf("END OF PACKET\n\n");
		cmp.push(opobj(0,END));
		eop_count++;
	}
	else
	{
		total_packets = b.getValue(11);
		//printf("--processOperand:: Total Packets = %d\n", total_packets);
		while (total_packets > 0)
		{
			
			total_packets--;
			processPacket(cmp, b);
		}
		//printf("END OF PACKET\n\n");
		cmp.push(opobj(0,END));
		eop_count++;
	}
	return sb;
}
	

int processPacket(comp &cmp, bitC &b)
{
// bitC b
//    int version = b.getValue(3);
	int version = b.getValue(3);
	sum_version += version;
//	  int type = b.getValue(3);
	int	type = b.getValue(3);
	//printf("\nProcess Packet:: version: %d  type: %d\n", version, type);
	if (type == 4)
	    processLiteral(cmp, b);
	else
		processOperand(cmp, (op_type) type, b);
	return sum_version;
}

bool ishex(char c)
{
	if ( ( (c >= '0') && (c <= '9') ) ||
		 ( (c >= 'A') && (c <= 'F') ) ) return true;
	return false;
}

// main
// init bits with file
//
#define MAXB 100
void  init(FILE *f)
{
	bitC  bc;
	char  c = 'A';
	char  b[MAXB];
	comp  cmp;
	while ( !feof(f) && ishex(c) )
	{
		c = fgetc(f);
		bc.addChar(c);
	}
	// get answer
	fgets(b, MAXB, f);
	int64_t expected = atol(b);
	//bc.out();
	printf("\n\nExpected answer: %ld\n", expected);
	sum_version = 0;
	processPacket(cmp, bc);
	printf("Version sum: %d\n", sum_version);
	//cmp.out();
	int64_t  comp_val = cmp.evaluate();
	printf("Compute: %ld\n", comp_val);
	if (comp_val == expected)
	    printf("****** CORRECT ANSWER ********\n");
	else
	    printf("-------- INCORRECT ANSWER ---------\n");

}

int	procFile(const char *fn, int n)
{
	FILE *f = fopen(fn, "r");
	while (n > 0){
	    init(f);
	    //printf("oper_count: %d    eop_count: %d\n", oper_count, eop_count);
		//evaluate();
	    n--;
	}
	return 0;
}


int main(int argc, char **argv)
{
	procFile("exp2.txt", 7);
	procFile("data.txt", 1);
	return 1;
}

/*
+(*(345367612077,>(848322,3213630547))*(=(14871,863441)1845)*(48216,<(+(12,14,10)+(12,15,4)))
M(29054,47144)*(238,>(1820,141))*(87,<(+(12,11,6)+(14,5,14)))*(196)657596,9,m(6794974,163690,737800,110541992,3)
*(=(29725,2480)37614)15811746,*(163,201,79,26,192)*(<(5691913,1618)15525854)*(>(3066,5890575)3931)*(128,144)
*(>(254374,179)172)+(13,14)*(88,>(500,500))56,*(40,177,48)*(+(10,3,12)+(9,7,15)+(10,13,4))*(>(184,184)61)m(224824157,6)
*(*(+(M(+(+(m(m(*(+(*(M(M(M(+(M(+(M(*(M(43))))))))))))))))))))375791589211,m(176,438,2272)*(3371,<(24870,192))12,20626,
m(5,61802,252,7340639596723)m(175)*(<(35841,35841)1)10,*(<(667983,2479419)3976415)+(*(6,12,3)*(7,8,10)*(2,8,4))
*(<(295267,295267)8)M(58535,4014590532,34,53086862385,953513)M(239,283,729288,42295)+(91,439363,241228265121,3314,817546689292)
M(242657,80,369780)*(>(+(15,15,11)+(4,6,10))118)+(2946,16851,114)2,15,*(=(44164,44164)26058)*(7,<(358,10411184))
+(4,2348,48212975426,215553481)*(>(+(15,11,13)+(6,4,4))136)*(=(+(9,11,7)+(10,11,13))5763)+(1747)*(2,167,137,26)M(2517))
* */

