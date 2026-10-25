CREATE DATABASE IF NOT EXISTS homefix_db;
USE homefix_db;

CREATE TABLE IF NOT EXISTS troubleshooting_rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    appliance VARCHAR(80) NOT NULL,
    symptom VARCHAR(160) NOT NULL,
    possible_cause TEXT NOT NULL,
    solution TEXT NOT NULL,
    safety_warning TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS repair_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    appliance VARCHAR(80) NOT NULL,
    symptom VARCHAR(255) NOT NULL,
    result_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO troubleshooting_rules (appliance, symptom, possible_cause, solution, safety_warning) VALUES
('AC','not cooling','Incorrect temperature setting, blocked air filter, or doors/windows allowing warm air inside.','Set cooling mode and a suitable temperature. Check that doors and windows are closed. Clean the user-removable filter only as described in the manual. If cooling does not improve, contact a technician.','Switch off before cleaning. Never open electrical panels or handle refrigerant lines.'),
('AC','not starting','Power supply issue, remote batteries, or a timer setting.','Check the wall switch and breaker without touching exposed wiring. Replace remote batteries and check timer settings. If it still does not start, contact service.','Do not repeatedly reset a tripping breaker or touch exposed wires.'),
('Refrigerator','not cooling','Air vents may be blocked, door may not close, or temperature setting may be incorrect.','Check the temperature setting, keep vents clear, and make sure the door seal closes properly. If food is warming, move it to safe cold storage and call service.','Do not remove the rear panel or touch compressor wiring.'),
('Refrigerator','making noise','Items may be touching each other or the appliance may not be level.','Move containers apart and check that the refrigerator stands evenly, following its manual. If loud or new noises continue, contact service.','Do not tilt or dismantle the refrigerator by yourself.'),
('Washing Machine','not starting','Door may not be fully closed, child lock may be on, or power may be unavailable.','Close the door firmly, check child lock and selected cycle, and verify the wall switch. Try again once.','Never bypass the door lock or touch wiring.'),
('Washing Machine','not draining','Drain hose may be kinked or the selected cycle may not have finished.','Check the cycle status and look for a visible kink in the external drain hose. Follow the manual for filter checks; otherwise contact a technician.','Switch off first. Water may be hot; do not remove parts if unsure.'),
('Fan','not working','Power switch, regulator, or remote batteries may be the cause.','Check the switch, regulator setting, and remote batteries. If the fan remains still, arrange professional service.','Do not touch blades or wiring. Never climb or dismantle a ceiling fan while powered.'),
('Fan','making noise','Loose external fittings or dust may cause noise.','Turn it off. Clean accessible surfaces according to the manual and check for visible wobbling from a safe distance. If noise continues, contact service.','Do not tighten electrical fittings or climb to repair a ceiling fan.'),
('Microwave','not heating','Incorrect mode, unsuitable settings, or an internal fault.','Check the selected mode and follow the manual. If it runs but does not heat, contact an authorized service centre.','Never open a microwave casing; dangerous voltage can remain even when unplugged.'),
('Water Heater','not heating','Power setting, thermostat setting, or a service fault may be responsible.','Check the user controls and manual. If the water remains cold, contact a qualified technician.','Water and electricity are dangerous together. Do not open the unit or touch wet switches.');
USE homefix_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);