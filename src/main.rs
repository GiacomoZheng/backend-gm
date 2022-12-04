use clap::Parser;
use backend_gm::Name;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// cmd
    cmd: String,

    /// path to the file
    name: String,
}


fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Cli::parse();

    let name = Name::from(args.name.as_str(), "/Users/giacomo/storage/GitHub");


    let content = std::fs::read_to_string(name.get_path()?)?;

    println!("{}", &content);

    Ok(())
}

