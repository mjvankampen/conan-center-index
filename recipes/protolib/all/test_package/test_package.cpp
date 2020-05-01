#include <protolib/protoApp.h>
#include <iostream>

int main()
{
	ProtoAddress localAddress;
    
    if (localAddress.ResolveLocalAddress())
    {
        std::cout << "local default IP address: " << localAddress.GetHostString() << std::endl;
		return EXIT_SUCCESS;
	}
	else
	{
		return EXIT_FAILURE;
	}
}
