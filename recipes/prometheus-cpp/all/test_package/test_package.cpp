#ifdef ENABLE_PULL

#include <prometheus/exposer.h>

#endif

#include <prometheus/counter.h>
#include <prometheus/registry.h>

#include <string>
#include <iostream>
#include <cstdlib>

int main(int argc, char *argv[])
{
    using namespace prometheus;

#ifdef ENABLE_PULL
    // create an http server running on port 8080
    Exposer exposer{"127.0.0.1:8081"};
#endif

    // create a metrics registry with component=main labels applied to all its
    // metrics
    auto registry = std::make_shared<Registry>();

    // add a new counter family to the registry (families combine values with the
    // same name, but distinct label dimensions)
    auto& counter_family = BuildCounter()
            .Name("time_running_seconds_total")
            .Help("How many seconds is this server running?")
            .Labels({{"label", "value"}})
            .Register(*registry);

    // add a counter to the metric family
    auto& second_counter = counter_family.Add(
            {{"another_label", "value"}, {"yet_another_label", "value"}});

    std::cout << "Tested prometheus-cpp - ok " << std::endl;

    return EXIT_SUCCESS;
}

