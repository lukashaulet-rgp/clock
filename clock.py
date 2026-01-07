print("")
print("Horloge en cours... (Ctrl+C pour arrêter)")
print("")

try:
    while True:
        
        if heure_personnalisee is not None:
            heures, minutes, secondes = heure_personnalisee
            heure_personnalisee = incrementer_heure(heures, minutes, secondes)
        else:
            maintenant = datetime.now()
            heures = maintenant.hour
            minutes = maintenant.minute
            secondes = maintenant.second
        
        print(f"\r{heures:02d}:{minutes:02d}:{secondes:02d}", end="", flush=True)
        
        if alarme is not None:
            if (heures, minutes, secondes) == alarme:
                print("\nDRIIIING ! C'est l'heure Mamie Jeannine !")
        
        time.sleep(1)

except KeyboardInterrupt:
    pass