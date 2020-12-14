#include <ppconsul/agent.h>
#include <ppconsul/status.h>
#include <ppconsul/kv.h>

#include <string>
#include <iostream>
#include <cstdlib>

using ppconsul::Consul;
using namespace ppconsul;
using namespace ppconsul::status;
using namespace ppconsul::agent;
using namespace ppconsul::kv;
using ConsulAgent=Agent;
using ConsulKv=Kv;

int main(int argc, char *argv[])
{
    Consul consul;
    ConsulAgent agent(consul);
    ConsulKv kv(consul);

    std::cout << "Tested ppconsul - ok " << std::endl;

    return EXIT_SUCCESS;
}