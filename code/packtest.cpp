#include <iostream>
#include <string>
#include <cstdio>
#include <cstring>

using namespace std;

// IP header structure
typedef struct _iphdr
{
  //Suppose the BYTE_ORDER is LITTLE_ENDIAN
  unsigned int   h_len:4;                // Length of the header
  unsigned int   version:4;              // Version of IP

  // ---------------------------------------------------------------
  // // Some padding on Windows 7/cl, char pad[3];
  // // No padding on Linux/cygwin/gcc
  // unsigned char  tos;                    // Type of service
  // unsigned short total_len;              // Total length of the packet

  // // No padding on both platforms
  unsigned int   tos:8;                  // Type of service
  unsigned int   total_len:16;           // Total length of the packet
  // ---------------------------------------------------------------

  unsigned short id;                     // Unique identification
  // unsigned short flags:3;                // Flags
  // unsigned short frag_offset:13;         // Fragment offset
  unsigned short frag_offset:13;         // Fragment offset
  unsigned short flags:3;                // Flags
  // unsigned short flags_frag_offset;      // F
  unsigned char  ttl;                    // Time to live
  unsigned char  protocol;               // Protocol (TCP, UDP etc)
  unsigned short checksum;               // IP checksum
  unsigned int   source_ip;              // Source IP
  unsigned int   dest_ip;                // Destination IP
} IpHeader;

int main(int argc, char *argv[])
{
  IpHeader iph;

  cout << sizeof(iph) << endl;
  for (size_t i = 0; i < sizeof(iph); ++i)
  {
    // *((char *)&iph + i) = 0x22 & 0xff;
    *((char *)&iph + i) = i & 0xff;
  }
  for (size_t i = 0; i < sizeof(iph); ++i)
  {
    printf("%02x ", *((char *)&iph + i));
  }
  cout << endl;
  cout << hex
       << iph.h_len << " "
       << iph.version << " "
       << (int)iph.tos << " "
       << iph.total_len << endl
       << iph.id << " "
       << iph.flags << " "
       << iph.frag_offset << endl
      // << iph.flags_frag_offset << endl
       << (int)iph.ttl << " "
       << (int)iph.protocol << " "
       << iph.checksum << endl
       << iph.source_ip << endl
       << iph.dest_ip << endl;

  return 0;
}
