use std::collections::VecDeque;
use std::path::{Path, PathBuf};

fn transparent(s: &PathBuf) -> bool {
	s.starts_with("_") && s.ends_with("_")
}

trait GmFile {
	fn is_gmfile(&self) -> bool;
	fn to_gm_path(&self) -> PathBuf;
}

impl GmFile for Path {
	fn is_gmfile(&self) -> bool {
		if self.is_dir() {
			// eprintln!("{:?}", self.join(".gm"));
			self.join(".gm").is_file()
		} else {
			// eprintln!("{:?}", self.join(".gm"));
			Path::new(&format!("{}{}", self.as_os_str().to_str().unwrap(), ".gm")).is_file()
		}
	}

	fn to_gm_path(&self) -> PathBuf {
		if self.is_dir() {
			self.join(".gm")
		} else {
			Path::new(&format!("{}{}", self.as_os_str().to_str().unwrap(), ".gm")).to_path_buf()
		}
	}
}

#[test]
fn gmfile() {
	assert!(Path::new("/Users/giacomo/storage/GitHub/gm").is_gmfile())
}

pub struct Name<'a> {
	inner : VecDeque<&'a str>,
	root: &'a Path
}
impl<'a> Name<'a> {
	pub fn from(s: &'a str, root: &'a str) -> Name<'a> {
		Name {
			inner: s.split(".").collect(),
			root: Path::new(root)
		}
	}

	pub fn forename(&self) -> &'a str {
		self.inner[(self.inner).len() - 1]
	}

	pub fn get_path(&self) -> Result<PathBuf, &'static str> {
		let mut dir = PathBuf::new();
		Name::analyze(self.root, &mut dir, &mut self.inner.clone())?;
		Ok(self.root.join(&dir).to_gm_path())
	}
	fn analyze(root: &'a Path, dir: &'a mut PathBuf, restname: &mut VecDeque<& str>) -> Result<(), &'static str> {
		if restname.is_empty() {
			if root.join(&dir).is_gmfile() {
				eprintln!("1");
				Ok(())
			} else {
				eprintln!("1'");
				Err("no such file (finally)")
			}

		} else if root.join(&dir).join(restname[0]).is_gmfile() {
			if let Some(e) = restname.pop_front() {
				dir.push(e);
			}
			eprintln!("2");
			Name::analyze(root, dir, restname)
		} else {
			for item in root.join(&dir).read_dir().expect("read_dir call failed").map(|x| x.unwrap().path()).filter(|x| transparent(x)) {
				eprintln!("3:{:?}", &item);
				eprintln!("{:?}", &item);
				if let Ok(()) = Name::analyze(root, &mut dir.join(&item), restname) {
					return Ok(());
				}
			}
			Err("no such file (half way)")
		}
	}
}



mod contents;
mod code;
mod size;