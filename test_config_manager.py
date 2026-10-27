from config_manager import save_config, load_config, get_config_path, config_exists


test_config = {
    "source_path": r"D:\TestSource",
    "backup_path": r"E:\TestBackup",
    "copies_to_keep": 10,
    "backup_frequency": "1 week",
    "first_backup_date": "29.09.2026",
    "first_backup_time": "18:00",
}


print("Config path:")
print(get_config_path())

print("\nConfig exists before save:")
print(config_exists())

print("\nSaving configuration...")
save_config(test_config)

print("\nConfig exists after save:")
print(config_exists())

print("\nLoaded configuration:")
print(load_config())