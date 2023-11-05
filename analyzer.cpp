namespace fs = std::filesystem;

void analyzer(){

    std::string path = "slimmed_ntuples/";
    for (const auto & entry : fs::directory_iterator(path))
        std::cout << entry.path() << std::endl;


}