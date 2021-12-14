use std::collections::HashMap;

const INPUT: &str = include_str!("input.txt");
const SAMPLE: &str = include_str!("sample.txt");

fn pass_days(fish_list: &[u8], days: usize) -> usize {
    // Keep a running tally of the number of fish at each stage of their lifecycle
    let mut fish_map: HashMap<u8, usize> = HashMap::new();

    // Populate the map with the initial list
    for fish in fish_list {
        let count = fish_map.entry(*fish).or_insert(0);
        *count += 1;
    }

    // Pass the days, shifting down the number of fish in each stage as we go
    for _ in 0..days {
        let mut prev_count = *fish_map.get(&0).unwrap_or(&0);
        for timer in (0..=8).rev() {
            if let Some(count) = fish_map.get_mut(&timer) {
                std::mem::swap(&mut prev_count, &mut (*count));
            } else {
                fish_map.insert(timer, prev_count);
                prev_count = 0;
            }
        }
        if let Some(count) = fish_map.get_mut(&6) {
            *count += prev_count;
        }
    }

    // Return the total number of fish in the map
    fish_map.values().sum()
}

fn main() {
    let sample_list: Vec<u8> = SAMPLE.trim().split(',').map(|x| {
        x.parse::<u8>().unwrap()
    }).collect();
    assert_eq!(pass_days(&sample_list, 80), 5934);
    assert_eq!(pass_days(&sample_list, 256), 26984457539);

    let input_list: Vec<u8> = INPUT.trim().split(',').map(|x| {
        x.parse::<u8>().unwrap()
    }).collect();
    println!("After 80 days, we have {} lanternfish", pass_days(&input_list, 80));
    println!("After 256 days, we have {} lanternfish", pass_days(&input_list, 256));
}

