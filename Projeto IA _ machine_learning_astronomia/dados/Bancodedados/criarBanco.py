import os
import sqlite3

# Garante o caminho absoluto onde o ficheiro .sqlite será criado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "DadosAstronomico.sqlite")

# Script SQL exato com a correção da vírgula final na tabela galaxyCluster
SQL_SCHEMA = """
CREATE TABLE IF NOT EXISTS star (
    idStar INTEGER PRIMARY KEY AUTOINCREMENT,
    nameStar TEXT NOT NULL,
    spectralClass TEXT NOT NULL,
    mainSpectralClass TEXT NOT NULL,
    evolutionaryStage TEXT NOT NULL,
    distanceStar_LY FLOAT NOT NULL,
    temperatureStar_K FLOAT NOT NULL,
    luminosityStar_logSun FLOAT NOT NULL,
    radiusStar_logSun FLOAT NOT NULL,
    massStar_logSun FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS starCluster (
    idStarCluster INTEGER PRIMARY KEY AUTOINCREMENT,
    nameStarCluster TEXT NOT NULL,
    typeStarCluster TEXT NOT NULL,
    distanceStarCluster_LY FLOAT NOT NULL,
    ageStarCluster_GYL FLOAT NOT NULL,
    estimatedStarsCountStarCluster FLOAT NOT NULL,
    coreRadius_PC FLOAT NOT NULL,
    tidalRadius_PC FLOAT NOT NULL,
    massStarCluster_logSun FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS superStarCluster (
    idSuperStarCluster INTEGER PRIMARY KEY AUTOINCREMENT,
    nameSuperStarCluster TEXT NOT NULL,
    hostGalaxySuperStarCluster TEXT NOT NULL,
    effectiveRadiusSuperStarCluster_pc FLOAT NOT NULL,
    ageSuperStarCluster_myr FLOAT NOT NULL,
    totalMassSuperStarCluster_logSun FLOAT NOT NULL,
    starFormationRateSuperStarCluster_sun_y FLOAT NOT NULL,
    centralDensitySuperStarCluster_M_sun_pc3 FLOAT NOT NULL,
    luminositySuperStarCluster_logSun FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS galaxy (
    idGalaxy INTEGER PRIMARY KEY AUTOINCREMENT,
    nameGalaxy TEXT NOT NULL,
    hubbleTypeGalaxy TEXT NOT NULL,
    generalMorphologyGalaxy TEXT NOT NULL,
    distanceGalaxy_LY FLOAT NOT NULL,
    effectiveRadiusGalaxy_KPC FLOAT NOT NULL,
    luminosityGalaxy_logSun FLOAT NOT NULL,
    starFormationRateGalaxy_Sun_Y FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS galaxyCluster (
    idGalaxyCluster INTEGER PRIMARY KEY AUTOINCREMENT,
    nameGalaxyCluster TEXT NOT NULL,
    morphologyTypeGalaxyCluster TEXT NOT NULL,
    distanceGalaxyCluster_LY TEXT NOT NULL,
    redShiftGalaxyCluster_z FLOAT NOT NULL,
    memberGalaxiesCountGalaxyCluster FLOAT NOT NULL,
    virialRadius_Mpc FLOAT NOT NULL,
    totalMassGalaxyCluster_logSun FLOAT NOT NULL,
    IntraclusterGasTemp_keV FLOAT NOT NULL,
    xRayLuminosity_erg_s FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS superGalaxyCluster (
    idSuperGalaxyCluster INTEGER PRIMARY KEY AUTOINCREMENT,
    nameSuperGalaxyCluster TEXT NOT NULL,
    cosmicStructureTypeSuperGalaxyCluster TEXT NOT NULL,
    distanceSuperGalaxyCluster_Mpc FLOAT NOT NULL,
    redshiftSuperGalaxyCluster_z FLOAT NOT NULL,
    memberClustersCount FLOAT NOT NULL,
    extentLength_Mpc FLOAT NOT NULL,
    totalMassGalaxyCluster_logSun FLOAT NOT NULL,
    overdensityFactor FLOAT NOT NULL
);
"""

def criar_banco():
    print(f"Criando base de dados em: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(SQL_SCHEMA)
    conn.commit()
    conn.close()
    print("Base de dados e tabelas criadas com sucesso! 🎉")

if __name__ == "__main__":
    criar_banco()